"""Validate all native-grid pairs and publish a local, static R2 data package."""

import argparse
import gzip
import itertools
import json
import math
import shutil
from collections import Counter
from pathlib import Path

import numpy as np
from osgeo import gdal

ROOT = Path(__file__).resolve().parents[1]
YEARS = list(range(2010, 2025))
R1 = ROOT / "web/public/data/r1"
OUT = ROOT / "web/public/data/r2"


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".part")
    tmp.write_text(json.dumps(value, ensure_ascii=False, allow_nan=False,
                              separators=(",", ":")) + "\n", encoding="utf-8")
    tmp.replace(path)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def counts(groups, codes):
    result = Counter()
    for group in groups:
        pair = divmod(int(group["pair"]), 100)
        area = group["sum"]
        if not set(pair) <= {0, *codes} or not math.isfinite(area) or area < 0:
            raise ValueError("Kode atau luas pasangan tidak valid.")
        result[pair] += area
    return result


def summarize(pairs, years):
    total = math.fsum(pairs.values())
    valid = {f"valid_{year}_ha": math.fsum(area for pair, area in pairs.items() if pair[i])
             for i, year in enumerate(years)}
    stable = math.fsum(area for (a, b), area in pairs.items() if a and a == b)
    changed = math.fsum(area for (a, b), area in pairs.items() if a and b and a != b)
    common = stable + changed
    excluded = math.fsum(v for (a, b), v in pairs.items() if not (a and b))
    if (abs(total - common - excluded) > 1e-6
        or common > min(valid.values()) + 1e-6
        or max(valid.values()) > total + 1e-6):
        raise ValueError("Neraca luas tidak konsisten.")
    return {"aoi_ha": total, **valid, "valid_common_ha": common, "stable_ha": stable,
            "changed_ha": changed, "not_comparable_ha": excluded,
            "changed_pct_common": 100 * changed / common if common else None}


def package_display(manifest, cache):
    tiles = sorted((cache / "tiles").glob("tile_*.tif"))
    if len(tiles) != 30:
        raise ValueError(f"Ubin raster belum lengkap {len(tiles)}/30")
    vrt = gdal.BuildVRT("", [str(p) for p in tiles])
    if (list(vrt.GetGeoTransform()) != manifest["raster"]["geotransform_gdal"]
        or [vrt.RasterXSize, vrt.RasterYSize] != manifest["raster"]["dimensions"] or vrt.RasterCount != 15):
        raise ValueError("Grid atau jumlah band raster R2 berbeda dari kontrak.")
    original = gdal.Open(str(R1 / manifest["raster"]["path"])).ReadAsArray()
    outside = original == 65535
    rasters = {}
    for i, year in enumerate(YEARS, 1):
        pixels = vrt.GetRasterBand(i).ReadAsArray()
        if not np.isin(pixels, [0, 255, *manifest["class_order"]]).all() or not np.array_equal(pixels == 255, outside):
            raise ValueError(f"Kelas atau cakupan raster berbeda {year}")
        if year in (2010, 2024):
            ref = original // 100 if year == 2010 else original % 100
            if not np.array_equal(pixels[~outside], ref[~outside]):
                raise ValueError(f"Raster R1 tidak sama {year}")
        rasters[str(year)] = gzip.compress(pixels.tobytes(), mtime=0)
    OUT.mkdir(parents=True, exist_ok=True)
    for year, packed in rasters.items():
        target = OUT / f"class_{year}.u8.gz"
        temp = target.with_suffix(".part")
        temp.write_bytes(packed)
        temp.replace(target)
    return rasters


def main():
    global OUT
    gdal.UseExceptions()
    manifest = read(R1 / "manifest.json")
    codes = manifest["class_order"]
    audit = read(ROOT / "data/metadata/r2_audit.json")
    cache = ROOT / "data/interim/r2" / audit["cache_key"]
    manifest_target = OUT / "manifest.json"
    OUT = OUT / audit["cache_key"]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--display-only", action="store_true")
    args = parser.parse_args()
    if args.display_only:
        rasters = package_display(manifest, cache)
        write(ROOT / "data/metadata/r2_display_qa.json", {
            "checked_on": "2026-11-17", "years": YEARS, "r1_endpoint_mismatch_pixels": 0,
            "grid": manifest["raster"], "gzip_bytes": {y: len(v) for y, v in rasters.items()},
            "validated_pixels_per_year": 13491162,
        })
        print("Raster 15 tahun siap. Grid, kode, mask luar AOI dan kedua ujung R1 lulus.", flush=True)
        return
    records = {r["region_id"]: {**r, "summary": {}, "annual_area_ha": {},
                               "annual_valid_ha": {}, "pairs": {}} for r in manifest["region_index"]}
    deltas = {}
    percentage_deltas = {}
    reconciliations = {}
    for before, after in itertools.combinations(YEARS, 2):
        key = f"{before}_{after}"
        aoi = counts(read(cache / f"{key}_aoi.json"), codes)
        rows = read(cache / f"{key}_district.json")
        districts = {r["properties"]["KDPKAB"]: r["properties"] for r in rows}
        expected = {rid for rid, r in records.items() if r["region_level"] == "district"}
        if set(districts) != expected or len(rows) != len(expected):
            raise ValueError(f"Daftar kabupaten berbeda {key}")
        zones = {"KALIMANTAN_ID": aoi}
        for rid, row in districts.items():
            if row["WADMKK"] != records[rid]["region_name"] or row["KDPPUM"] != records[rid]["province_id"]:
                raise ValueError(f"Atribut wilayah berbeda dari R1 {rid}")
            pair = counts(row["groups"], codes)
            zones[rid] = pair
            pid = records[rid]["province_id"]
            zones.setdefault(pid, Counter()).update(pair)
        for rid, pair in zones.items():
            summary = summarize(pair, (before, after))
            matrix = [[pair[a, b] for b in codes] for a in codes]
            if abs(math.fsum(v for row in matrix for v in row) - summary["valid_common_ha"]) > 1e-6:
                raise ValueError(f"Neraca transisi gagal {rid} {key}")
            record = records[rid]
            record["pairs"][key] = {"summary": summary, "transition_area_ha": matrix}
            for i, year in enumerate((before, after)):
                areas = [math.fsum(v for p, v in pair.items() if p[i] == c) for c in codes]
                previous = record["annual_area_ha"].get(str(year))
                if previous and max(abs(a - b) for a, b in zip(previous, areas)) > .01:
                    raise ValueError(f"Luas tahunan lintas pasangan berbeda {rid} {year}")
                record["annual_area_ha"][str(year)] = areas
                record["annual_valid_ha"][str(year)] = summary[f"valid_{year}_ha"]
            if key == "2010_2024":
                reference = read(R1 / record["stats"])
                differences = [abs(summary[k] - v) for k, v in reference["summary"].items()
                               if v is not None and k != "changed_pct_common"]
                pct_delta = abs(summary["changed_pct_common"] - reference["summary"]["changed_pct_common"])
                differences += [abs(a - b) for row, ref in zip(matrix, reference["transition_area_ha"])
                                for a, b in zip(row, ref)]
                if max(differences) > .01 or pct_delta > 1e-6:
                    raise ValueError(f"Regresi R1 gagal {rid}")
                deltas[rid] = max(differences)
                percentage_deltas[rid] = pct_delta
                record["summary"] = summary

        aoi_summary = records["KALIMANTAN_ID"]["pairs"][key]["summary"]
        delta = math.fsum(records[rid]["pairs"][key]["summary"]["aoi_ha"] for rid in expected) - aoi_summary["aoi_ha"]
        if abs(delta) > aoi_summary["aoi_ha"] * .001:
            raise ValueError(f"Selisih cakupan antartingkat terlalu besar {key}")
        reconciliations[key] = delta

    rasters = package_display(manifest, cache)
    for r in records.values():
        write(OUT / r["stats"], r)
    for boundary in manifest["boundaries"].values():
        shutil.copyfile(R1 / boundary["path"], OUT / boundary["path"])
        boundary["path"] = f"{cache.name}/{boundary['path']}"
    for region in manifest["region_index"]:
        region["stats"] = f"{cache.name}/{region['stats']}"
    manifest.update(release="R2", years=YEARS, pairs=[f"{a}_{b}" for a, b in itertools.combinations(YEARS, 2)])
    manifest["raster"].update(encoding="one UInt8 class per pixel per year; 255 outside AOI; 0 invalid",
                              year_paths={y: f"{cache.name}/class_{y}.u8.gz" for y in rasters})
    manifest["raster"].pop("path")
    manifest["raster"].update(nodata_outside_aoi=255, format="gzip UInt8")
    manifest["statistics"]["reconciliation_reference_pair"] = "2010_2024"
    manifest["build_id"] = cache.name
    write(manifest_target, manifest)
    aoi_record = records["KALIMANTAN_ID"]
    annual_audit = {}
    for year in YEARS:
        valid = aoi_record["annual_valid_ha"][str(year)]
        area = aoi_record["summary"]["aoi_ha"]
        annual_audit[str(year)] = {"area_ha": aoi_record["annual_area_ha"][str(year)],
                                   "valid_ha": valid, "aoi_ha": area, "valid_pct": 100 * valid / area}
    write(ROOT / "data/metadata/r2_annual_qa.json", {
        "checked_on": "2026-11-17", "class_order": codes, "aoi": annual_audit,
        "method": "native grid Earth Engine pixelArea; class remap uses audited valid codes",
    })
    write(ROOT / "data/metadata/r2_package_qa.json", {
        "checked_on": "2026-11-17", "years": len(YEARS), "regions": len(records), "pairs": 105,
        "annual_cells": len(records) * len(YEARS) * len(codes),
        "transition_cells": len(records) * 105 * len(codes)**2,
        "r1_max_difference_ha": max(deltas.values()), "raster_endpoint_mismatch_pixels": 0,
        "r1_max_changed_share_difference_percentage_points": max(percentage_deltas.values()),
        "compressed_raster_bytes": {y: len(b) for y, b in rasters.items()},
        "strategy": "15 yearly rasters loaded on demand; native-grid matrices for all 105 pairs",
        "district_sum_minus_aoi_area_ha_by_pair": reconciliations,
    })
    print("Paket R2 lengkap dan regresi R1 lulus.", flush=True)


if __name__ == "__main__":
    main()
