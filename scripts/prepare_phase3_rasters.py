"""Construct Phase 4 inputs on the audited MapBiomas grid; verify and download QA windows."""

import argparse
import json
import math
from collections import Counter
from pathlib import Path

import ee
import requests

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "config/project.example.json").read_text(encoding="utf-8"))
PROJECT = CONFIG["region"]["boundary_asset_id"].split("/")[1]
GRID = CONFIG["analysis"]["crs_transform"]
CRS = CONFIG["analysis"]["crs"]
CODES = CONFIG["analysis"]["valid_class_codes"]
PILOT = tuple(CONFIG["period"]["pilot_years"])


def prepare(years=PILOT):
    """Return boundary, source classifications, yearly masks and common mask in Earth Engine."""
    years = tuple(years)
    period = CONFIG["period"]
    if (not years or len(set(years)) != len(years)
        or any(y < period["start"] or y > period["end"] for y in years)):
        raise ValueError("Gunakan tahun unik dalam periode proyek 2010–2024.")
    boundary = ee.FeatureCollection(CONFIG["region"]["boundary_asset_id"])
    source = ee.Image(CONFIG["mapbiomas"]["asset_id"])
    classes = {
        year: source.select(f"classification_{year}").rename(f"class_{year}").clipToCollection(boundary)
        for year in years
    }
    valid = {
        year: image.remap(CODES, [1] * len(CODES), 0).unmask(0, False)
        .toByte().rename(f"valid_{year}").clipToCollection(boundary)
        for year, image in classes.items()
    }
    common = valid[years[0]]
    for year in years[1:]:
        common = common.And(valid[year])
    common = common.rename("valid_common").toByte()
    aoi = ee.Image.constant(1).rename("in_aoi").toByte().clipToCollection(boundary)
    return boundary, classes, valid, common, aoi


def verify_and_download():
    """Verify existing inputs without creating cloud assets or rerunning full-area statistics."""
    ee.Initialize(project=PROJECT)
    ee.data.setDeadline(45000)
    boundary, classes, valid, common, aoi = prepare()
    boundary_rows = boundary.map(lambda f: ee.Feature(None, f.toDictionary(
        ["KDPKAB", "WADMKK", "KDPPUM", "WADMPR"]
    ))).getInfo()["features"]
    counts = Counter(row["properties"]["KDPPUM"] for row in boundary_rows)
    districts = [row["properties"]["KDPKAB"] for row in boundary_rows]
    if len(districts) != len(set(districts)) or counts != {"61": 14, "62": 14, "63": 13, "64": 10, "65": 5}:
        raise ValueError(f"Atribut aset batas berbeda dari cakupan kerja: {counts}")

    source = ee.Image(CONFIG["mapbiomas"]["asset_id"])
    all_years = range(CONFIG["period"]["start"], CONFIG["period"]["end"] + 1)
    names = [f"classification_{year}" for year in all_years]
    band_info = source.select(names).getInfo()["bands"]
    if len(band_info) != len(names) or any(
        band["crs"] != CRS or any(
            not math.isclose(a, b, rel_tol=0, abs_tol=1e-12)
            for a, b in zip(band["crs_transform"], GRID, strict=True)
        ) for band in band_info
    ):
        raise ValueError("Grid salah satu band 2010–2024 berbeda dari grid acuan.")

    stack = ee.Image.cat(*[
        *[classes[y].updateMask(valid[y]) for y in PILOT],
        *[valid[y] for y in PILOT], common, aoi,
    ]).unmask(255, False).toByte()
    output = ROOT / "data/processed/phase3_qa"
    output.mkdir(parents=True, exist_ok=True)
    names_preview = ["class_2010", "class_2024", "valid_2010", "valid_2024", "valid_common", "in_aoi"]
    report = {
        "project": PROJECT,
        "mapbiomas_asset": CONFIG["mapbiomas"]["asset_id"],
        "boundary_asset": CONFIG["region"]["boundary_asset_id"],
        "district_codes": sorted(districts),
        "province_counts": dict(sorted(counts.items())),
        "verified_grid_bands": names,
        "crs": CRS,
        "grid_transform": GRID,
        "preview_band_order": names_preview,
        "preview_mask_sentinel": 255,
        "previews": {},
    }
    points = {
        "sawit_2024": (116.11180945083655, -2.0012525891793755),
        "perbatasan": (114.72883058473096, 1.834314894407858),
    }
    for label, (lon, lat) in points.items():
        col = math.floor((lon - GRID[2]) / GRID[0])
        row = math.floor((lat - GRID[5]) / GRID[4])
        transform = [GRID[0], 0, GRID[2] + (col - 64) * GRID[0],
                     0, GRID[4], GRID[5] + (row - 64) * GRID[4]]
        url = stack.getDownloadURL({
            "crs": CRS, "crs_transform": transform, "dimensions": [128, 128],
            "format": "GEO_TIFF", "filePerBand": False,
        })
        response = requests.get(url, timeout=90)
        if not response.ok or response.content[:4] not in (b"II*\x00", b"MM\x00*"):
            raise RuntimeError(f"GeoTIFF QA gagal diunduh: {label}, HTTP {response.status_code}")
        target = output / f"{label}.tif"
        partial = target.with_suffix(".part")
        partial.write_bytes(response.content)
        partial.replace(target)
        report["previews"][label] = {
            "path": target.relative_to(ROOT).as_posix(), "point": [lon, lat],
            "shape": [128, 128], "transform": transform,
        }
        print(f"Jendela QA tersimpan: {label}", flush=True)
    (ROOT / "data/metadata/phase3_raster_qa.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", action="store_true", required=True)
    parser.parse_args()
    verify_and_download()
