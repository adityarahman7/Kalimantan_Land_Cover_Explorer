"""Resumable native-grid R2 pair reductions and annual metadata audit."""

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

import ee

from analyze_phase4 import BOUNDS, FIELDS, read_pairs, write_json
from prepare_phase3_rasters import CONFIG, CODES, CRS, GRID, PROJECT, ROOT

YEARS = list(range(2010, 2025))
CACHE = ROOT / "data/interim/r2"


def audit():
    source = ee.Image(CONFIG["mapbiomas"]["asset_id"])
    assets = [ee.data.getAsset(CONFIG["mapbiomas"]["asset_id"]),
              ee.data.getAsset(CONFIG["region"]["boundary_asset_id"])]
    bands = source.select([f"classification_{y}" for y in YEARS]).getInfo()["bands"]
    assert len(bands) == 15
    for band in bands:
        assert band["crs"] == CRS
        assert all(math.isclose(a, b, abs_tol=1e-12, rel_tol=0)
                   for a, b in zip(band["crs_transform"], GRID, strict=True))
    boundary = ee.FeatureCollection(CONFIG["region"]["boundary_asset_id"])
    rows = boundary.map(lambda f: ee.Feature(None, f.toDictionary(FIELDS))).getInfo()["features"]
    expected = json.loads((ROOT / "data/metadata/phase3_raster_qa.json").read_text())
    assert sorted(r["properties"]["KDPKAB"] for r in rows) == expected["district_codes"]
    key = hashlib.sha256(json.dumps([assets, CONFIG, "r2-native-pairs-v1"],
                                    sort_keys=True).encode()).hexdigest()[:16]
    report = {"checked_on": "2026-11-17", "cache_key": key, "years": YEARS,
              "grid": GRID, "crs": CRS, "district_count": len(rows),
              "asset_id": CONFIG["mapbiomas"]["asset_id"], "asset_metadata": assets,
              "valid_codes": CODES, "pair_count": 105}
    write_json(ROOT / "data/metadata/r2_audit.json", report)
    return boundary, source, CACHE / key


def compute_pair(years, boundary, source, folder):
    before, after = years
    name = f"{before}_{after}"
    outputs = [folder / f"{name}_{level}.json" for level in ("aoi", "district")]
    if all(p.exists() for p in outputs):
        return name
    classes = [source.select(f"classification_{y}").remap(CODES, CODES, 0)
               .unmask(0, False).toInt16() for y in years]
    paired = classes[0].multiply(100).add(classes[1]).rename("pair")
    image = ee.Image.pixelArea().divide(10000).addBands(paired)
    reducer = ee.Reducer.sum().group(groupField=1, groupName="pair")
    grid = dict(crs=CRS, crsTransform=GRID, tileScale=1)
    if not outputs[0].exists():
        result = image.clipToCollection(boundary).reduceRegion(reducer, ee.Geometry.Rectangle(BOUNDS, geodesic=False),
                                    maxPixels=10**10, **grid).getInfo()["groups"]
        read_pairs(result)
        write_json(outputs[0], result)
    if not outputs[1].exists():
        result = image.reduceRegions(boundary, reducer, maxPixelsPerRegion=10**10, **grid)
        rows = result.map(lambda f: ee.Feature(None, f.toDictionary(FIELDS + ["groups"]))).getInfo()["features"]
        expected = json.loads((ROOT / "data/metadata/phase3_raster_qa.json").read_text())
        assert sorted(r["properties"]["KDPKAB"] for r in rows) == expected["district_codes"]
        for row in rows:
            read_pairs(row["properties"]["groups"])
        write_json(outputs[1], rows)
    print(f"Pasangan selesai {name}", flush=True)
    return name


def sample_classes(boundary, source):
    bands = [f"classification_{y}" for y in YEARS]
    rows = source.select(bands).clipToCollection(boundary).sample(
        region=ee.Geometry.Rectangle(BOUNDS, geodesic=False), projection=ee.Projection(CRS, GRID),
        numPixels=1200, seed=23, dropNulls=False, geometries=False, tileScale=2).getInfo()["features"]
    counts = {str(y): dict(Counter(str(r["properties"].get(band)) for r in rows))
              for y, band in zip(YEARS, bands)}
    allowed = {str(code) for code in [*CODES, 27]} | {"None"}
    unknown = sorted({code for values in counts.values() for code in values if code not in allowed})
    report = {"checked_on": "2026-11-17", "requested_points": 1200, "returned_points": len(rows),
              "seed": 23, "histograms": counts, "unexpected_codes": unknown,
              "limitation": "Diagnostic random sample, not complete class inventory or accuracy assessment"}
    write_json(ROOT / "data/metadata/r2_class_sample_qa.json", report)
    if unknown:
        raise ValueError(f"Kode tambahan perlu diaudit: {unknown}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--audit-only", action="store_true")
    parser.add_argument("--baseline", action="store_true", help="All years against 2010")
    parser.add_argument("--remaining", action="store_true")
    parser.add_argument("--regression", action="store_true")
    parser.add_argument("--workers", type=int, choices=range(1, 9), default=4)
    parser.add_argument("--sample-classes", action="store_true")
    args = parser.parse_args()
    ee.Initialize(project=PROJECT)
    ee.data.setDeadline(280000)
    boundary, source, folder = audit()
    print(f"Audit grid dan 56 kode wilayah lulus. Cache {folder.name}", flush=True)
    if args.sample_classes:
        sample_classes(boundary, source)
    if args.audit_only:
        return
    if args.regression:
        compute_pair((2010, 2024), boundary, source, folder)
        return
    if args.remaining:
        pairs = list(itertools.combinations(YEARS[1:], 2))
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            list(pool.map(lambda pair: compute_pair(pair, boundary, source, folder), pairs))
        return
    pairs = ([(2010, y) for y in YEARS[1:]] if args.baseline
             else list(itertools.combinations(YEARS, 2)))
    pairs.sort(key=lambda pair: (pair != (2010, 2024), pair[0] != 2010, pair))
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        list(pool.map(lambda pair: compute_pair(pair, boundary, source, folder), pairs))



if __name__ == "__main__":
    main()

