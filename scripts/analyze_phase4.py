"""Pilot R1 area and transition tables on the audited Earth Engine grid."""
import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import ee
import requests

from prepare_phase3_rasters import CODES, CONFIG, CRS, GRID, PILOT, PROJECT, ROOT, prepare

OUT = ROOT / "outputs/tables/phase4"
CACHE = ROOT / "data/interim/phase4"
BOUNDS = [108.59, -4.95, 119.04, 4.42]
BASE = 100
AUDIT_TOLERANCE_HA = 1.0
AGGREGATION_TOLERANCE_FRACTION = 0.001
FIELDS = ["KDPKAB", "WADMKK", "KDPPUM", "WADMPR"]


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".part")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                   encoding="utf-8")
    tmp.replace(path)


def reduce_groups(boundary, paired):
    area = ee.Image.pixelArea().divide(10000).rename("hectares")
    image = area.addBands(paired).clipToCollection(boundary)
    reducer = ee.Reducer.sum().group(groupField=1, groupName="pair")
    grid = {"crs": CRS, "crsTransform": GRID, "tileScale": 4}
    # Cache successful requests so interrupted runs need not recompute every zone.
    assets = [
        ee.data.getAsset(CONFIG["mapbiomas"]["asset_id"]),
        ee.data.getAsset(CONFIG["region"]["boundary_asset_id"]),
    ]
    key = hashlib.sha256(json.dumps([assets, CONFIG, BOUNDS, BASE], sort_keys=True).encode()
                         + Path(__file__).read_bytes()).hexdigest()[:16]

    def cached(name, compute):
        path = CACHE / key / f"{name}.json"
        if not path.exists():
            write_json(path, compute())
        print(f"Siap: {name}", flush=True)
        return json.loads(path.read_text(encoding="utf-8"))

    def aoi():
        return cached("aoi", lambda: image.reduceRegion(
            reducer, ee.Geometry.Rectangle(BOUNDS, geodesic=False),
            maxPixels=10**10, **grid
        ).getInfo()["groups"])

    def province(province_id):
        zones = boundary.filter(ee.Filter.eq("KDPPUM", province_id))
        return cached(province_id, lambda: image.reduceRegions(
            zones, reducer, maxPixelsPerRegion=10**10, **grid
        ).map(lambda f: ee.Feature(None, f.toDictionary(FIELDS + ["groups"])))
          .getInfo()["features"])

    with ThreadPoolExecutor(max_workers=2) as pool:
        aoi_result = pool.submit(aoi)
        parts = list(pool.map(province, ["61", "62", "63", "64", "65"]))
        return aoi_result.result(), [f["properties"] for part in parts for f in part]


def read_pairs(groups):
    pairs = Counter()
    for group in groups:
        pair = divmod(int(group["pair"]), BASE)
        hectares = group["sum"]
        if not set(pair).issubset({0, *CODES}) or not math.isfinite(hectares) or hectares < 0:
            raise ValueError(f"Pasangan atau luas tidak valid: {group}")
        pairs[pair] += hectares
    if not pairs:
        raise ValueError("Wilayah tidak memiliki hasil reduksi.")
    return pairs


def percent(area, denominator):
    return 100 * area / denominator if denominator else None


def summarize(pairs):
    area = math.fsum(pairs.values())
    before = math.fsum(v for (a, _), v in pairs.items() if a)
    after = math.fsum(v for (_, b), v in pairs.items() if b)
    stable = math.fsum(v for (a, b), v in pairs.items() if a and a == b)
    changed = math.fsum(v for (a, b), v in pairs.items() if a and b and a != b)
    excluded = math.fsum(v for (a, b), v in pairs.items() if not (a and b))
    common = stable + changed
    if (not math.isclose(area, common + excluded, rel_tol=0, abs_tol=1e-6)
        or common > min(before, after) + 1e-6 or max(before, after) > area + 1e-6):
        raise ValueError("Neraca luas tidak konsisten.")
    return {
        "aoi_ha": area, "valid_2010_ha": before, "valid_2024_ha": after,
        "valid_common_ha": common, "stable_ha": stable, "changed_ha": changed,
        "not_comparable_ha": excluded, "changed_pct_common": percent(changed, common),
    }


def save_csv(name, records):
    path = OUT / f"{name}.csv"
    tmp = path.with_suffix(".part")
    with tmp.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    tmp.replace(path)


def build_tables(aoi_groups, districts):
    expected = json.loads((ROOT / "data/metadata/phase3_raster_qa.json").read_text(encoding="utf-8"))
    if sorted(row["KDPKAB"] for row in districts) != expected["district_codes"]:
        raise ValueError("Hasil reduksi tidak memuat tepat 56 kode kabupaten/kota fase 3.")
    aoi = read_pairs(aoi_groups)
    provinces = {}
    zones = [({"region_level": "aoi", "region_id": "KALIMANTAN_ID",
               "region_name": "Kalimantan Indonesia", "province_id": ""}, aoi)]
    for row in sorted(districts, key=lambda item: item["KDPKAB"]):
        pairs = read_pairs(row["groups"])
        pid = row["KDPPUM"]
        name, aggregate = provinces.setdefault(pid, (row["WADMPR"], Counter()))
        if name != row["WADMPR"]:
            raise ValueError(f"Nama provinsi tidak konsisten: {pid}")
        aggregate.update(pairs)
        zones.append(({"region_level": "district", "region_id": row["KDPKAB"],
                       "region_name": row["WADMKK"], "province_id": pid}, pairs))
    zones[1:1] = [({"region_level": "province", "region_id": pid,
                   "region_name": name, "province_id": pid}, pairs)
                  for pid, (name, pairs) in sorted(provinces.items())]

    summary, annual, transitions = [], [], []
    for zone, pairs in zones:
        totals = summarize(pairs)
        summary.append({**zone, "year_from": PILOT[0], "year_to": PILOT[1], **totals})
        for i, year in enumerate(PILOT):
            denominator = totals[f"valid_{year}_ha"]
            for code in CODES:
                area = math.fsum(v for pair, v in pairs.items() if pair[i] == code)
                annual.append({**zone, "year": year, "class_code": code, "area_ha": area,
                               "valid_ha": denominator, "share_pct_valid": percent(area, denominator)})
        for a in CODES:
            for b in CODES:
                area = pairs[a, b]
                transitions.append({**zone, "year_from": PILOT[0], "year_to": PILOT[1],
                                    "class_from": a, "class_to": b, "area_ha": area,
                                    "valid_common_ha": totals["valid_common_ha"],
                                    "share_pct_common": percent(area, totals["valid_common_ha"])})
    with (ROOT / "data/metadata/audit_cakupan_valid_2010_2024.csv").open(encoding="utf-8-sig") as file:
        reference = next(csv.DictReader(file))
    aoi_result = summary[0]
    fields = {"aoi_ha": "wilayah_ha", "valid_2010_ha": "valid_2010_ha",
              "valid_2024_ha": "valid_2024_ha", "valid_common_ha": "valid_bersama_ha"}
    differences = {field: aoi_result[field] - float(reference[source])
                   for field, source in fields.items()}
    if max(map(abs, differences.values())) > AUDIT_TOLERANCE_HA:
        raise ValueError(f"Hasil AOI berbeda dari audit di luar toleransi: {differences}")
    district_delta = {
        field: math.fsum(row[field] for row in summary if row["region_level"] == "district")
        - aoi_result[field] for field in [*fields, "stable_ha", "changed_ha", "not_comparable_ha"]
    }
    if max(map(abs, district_delta.values())) > aoi_result["aoi_ha"] * AGGREGATION_TOLERANCE_FRACTION:
        raise ValueError(f"Selisih agregasi antartingkat terlalu besar: {district_delta}")
    qa = {
        "aoi": aoi_result, "districts": len(districts), "provinces": len(provinces),
        "annual_rows": len(annual), "transition_rows": len(transitions),
        "aoi_minus_phase2_ha": differences, "audit_tolerance_ha": AUDIT_TOLERANCE_HA,
        "district_sum_minus_aoi_ha": district_delta,
        "aggregation_tolerance_fraction_of_aoi": AGGREGATION_TOLERANCE_FRACTION,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    save_csv("luas_kelas", annual)
    save_csv("transisi_kelas", transitions)
    save_csv("ringkasan_perubahan", summary)
    write_json(ROOT / "data/metadata/phase4_qa.json", qa)
    print(json.dumps(qa, ensure_ascii=False), flush=True)


def export_overview(boundary, web_pairs=False):
    """Download tiles for a categorical overview, independently of area statistics."""
    step = 10
    left = math.floor((BOUNDS[0] - GRID[2]) / (step * GRID[0]))
    top = math.floor((BOUNDS[3] - GRID[5]) / (step * GRID[4]))
    right = math.ceil((BOUNDS[2] - GRID[2]) / (step * GRID[0]))
    bottom = math.ceil((BOUNDS[1] - GRID[5]) / (step * GRID[4]))
    source = ee.Image(CONFIG["mapbiomas"]["asset_id"])
    before, after = [
        source.select(f"classification_{year}").remap(CODES, CODES, 0).unmask(0, False)
        for year in PILOT
    ]
    common = before.neq(0).And(after.neq(0))
    image_source = (
        before.multiply(BASE).add(after).rename("pair").toUint16() if web_pairs
        else ee.Image.constant(2).where(common, before.neq(after)).rename("change").toByte()
    )
    outside = 65535 if web_pairs else 255
    tile_size = 768
    folder = (ROOT / "data/interim/phase5/pair_tiles") if web_pairs else (CACHE / "overview_tiles")
    folder.mkdir(parents=True, exist_ok=True)

    def download(tile):
        x, y = tile
        width, height = min(tile_size, right-x), min(tile_size, bottom-y)
        dx, dy = step * GRID[0], step * GRID[4]
        west, north = GRID[2] + x * dx, GRID[5] + y * dy
        # Include a native pixel margin to avoid filtering out geometry at a tile edge.
        footprint = ee.Geometry.Rectangle([
            west - GRID[0], north + height * dy + GRID[4],
            west + width * dx + GRID[0], north - GRID[4],
        ], geodesic=False)
        image = image_source.clipToCollection(boundary.filterBounds(footprint)).unmask(outside, False)
        transform = [dx, 0, west, 0, dy, north]
        url = image.getDownloadURL({
            "crs": CRS, "crs_transform": transform, "dimensions": [width, height],
            "format": "GEO_TIFF", "filePerBand": False,
        })
        response = requests.get(url, timeout=150)
        if not response.ok or response.content[:4] not in (b"II*\x00", b"MM\x00*"):
            message = response.json().get("error", {}).get("message", "") if (
                "application/json" in response.headers.get("Content-Type", "")
            ) else ""
            raise RuntimeError(f"Tile {x},{y} gagal: HTTP {response.status_code} {message[:350]}")
        target = folder / f"tile_{y}_{x}.tif"
        tmp = target.with_suffix(".part")
        tmp.write_bytes(response.content)
        tmp.replace(target)
        print(f"Tile QA siap: {target.name}", flush=True)

    tiles = [(x, y) for y in range(top, bottom, tile_size)
             for x in range(left, right, tile_size)]
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(download, tiles))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--map-only", action="store_true",
                        help="Perbarui raster tinjauan tanpa mengulang reduksi luas.")
    modes.add_argument("--web-pairs-only", action="store_true",
                       help="Unduh ubin pasangan kelas R1 untuk paket web lokal.")
    args = parser.parse_args()
    ee.Initialize(project=PROJECT)
    ee.data.setDeadline(280000)
    boundary, classes, valid, _, _ = prepare()
    if not (args.map_only or args.web_pairs_only):
        before, after = [classes[y].updateMask(valid[y]).unmask(0, False).toInt16()
                         for y in PILOT]
        pairs = before.multiply(BASE).add(after).rename("pair")
        aoi_groups, districts = reduce_groups(boundary, pairs)
        build_tables(aoi_groups, districts)
    export_overview(boundary, web_pairs=args.web_pairs_only)


if __name__ == "__main__":
    main()
