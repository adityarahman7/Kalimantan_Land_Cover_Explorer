"""Package the R1 geospatial data for static WebGIS delivery (GDAL Python)."""

import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path

import numpy as np
from osgeo import gdal, ogr

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / "config/project.example.json").read_text(encoding="utf-8"))
CODES = CONFIG["analysis"]["valid_class_codes"]
YEARS = CONFIG["period"]["pilot_years"]
OUT = ROOT / "web/public/data/r1"
NODATA = 65535
LEGEND = {
    3: ("Formasi hutan", "#1f8d49"), 5: ("Mangrove", "#04381d"),
    9: ("Kebun kayu", "#7a5900"), 13: ("Tumbuhan non-hutan lainnya", "#d89f5c"),
    21: ("Pertanian lainnya", "#ffefc3"), 24: ("Permukiman", "#d4271e"),
    25: ("Nonvegetasi lainnya", "#db4d4f"), 30: ("Lubang tambang", "#9c0027"),
    31: ("Tambak", "#091077"), 33: ("Sungai, danau, laut", "#2532e4"),
    35: ("Sawit", "#9065d0"), 40: ("Sawah", "#f272c2"),
    76: ("Hutan rawa gambut", "#2f7360"),
}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".part")
    temp.write_text(json.dumps(value, ensure_ascii=False, allow_nan=False,
                               separators=(",", ":")) + "\n", encoding="utf-8")
    temp.replace(path)


def table(name):
    path = ROOT / "outputs/tables/phase4" / (name + ".csv")
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def package_stats():
    annual, transitions = defaultdict(dict), defaultdict(dict)
    for row in table("luas_kelas"):
        key = int(row["year"]), int(row["class_code"])
        annual[row["region_id"]][key] = float(row["area_ha"])
    for row in table("transisi_kelas"):
        key = int(row["class_from"]), int(row["class_to"])
        transitions[row["region_id"]][key] = float(row["area_ha"])

    index = []
    fields = ("aoi_ha", "valid_2010_ha", "valid_2024_ha", "valid_common_ha",
              "stable_ha", "changed_ha", "not_comparable_ha", "changed_pct_common")
    for row in table("ringkasan_perubahan"):
        rid = row["region_id"]
        if not re.fullmatch(r"[A-Za-z0-9_-]+(?:\.[A-Za-z0-9_-]+)*", rid):
            raise ValueError(f"ID wilayah tidak aman untuk nama berkas: {rid}")
        record = {key: row[key] or None for key in
                  ("region_id", "region_level", "region_name", "province_id")}
        record["stats"] = f"stats/{rid}.json"
        summary = {key: float(row[key]) if row[key] else None for key in fields}
        arrays = {str(y): [annual[rid][y, code] for code in CODES] for y in YEARS}
        matrix = [[transitions[rid][a, b] for b in CODES] for a in CODES]
        if any(abs(math.fsum(arrays[str(y)]) - summary[f"valid_{y}_ha"]) > 1e-6
               for y in YEARS):
            raise ValueError(f"Luas tahunan tidak seimbang: {rid}")
        if abs(math.fsum(v for values in matrix for v in values) - summary["valid_common_ha"]) > 1e-6:
            raise ValueError(f"Matriks tidak seimbang: {rid}")
        write_json(OUT / record["stats"], {
            **record, "summary": summary, "annual_area_ha": arrays,
            "transition_area_ha": matrix,
        })
        index.append(record)
    if (len(index) != 62 or len({r["region_id"] for r in index}) != 62
        or set(annual) != {r["region_id"] for r in index}
        or set(transitions) != {r["region_id"] for r in index}):
        raise ValueError("Daftar wilayah fase 4 tidak lengkap atau ID tidak unik.")
    return index


def package_boundaries(regions):
    source = ROOT / "data/processed/phase3_boundaries.gpkg"
    definitions = {
        "aoi": ("aoi", "aoi_id"), "province": ("provinsi", "province_id"),
        "district": ("kabupaten_kota", "district_id"),
    }
    result = {}
    for level, (layer, id_field) in definitions.items():
        name = f"{level}.geojson"
        tmp = OUT / f"{level}.part.geojson"
        output = gdal.VectorTranslate(str(tmp), str(source), options=gdal.VectorTranslateOptions(
            options=["-f", "GeoJSON", "-simplify", "0.001", "-dim", "XY",
                     "-lco", "RFC7946=YES", "-lco", "COORDINATE_PRECISION=7"],
            layers=[layer],
        ))
        if output is None:
            raise RuntimeError(f"Ekspor GeoJSON gagal: {level}")
        output = None
        ds = ogr.Open(str(tmp))
        actual = []
        for feature in ds.GetLayer(0):
            geom = feature.GetGeometryRef()
            if geom is None or geom.IsEmpty() or not geom.IsValid():
                raise ValueError(f"Geometri tampilan invalid: {level}")
            actual.append(feature[id_field])
        expected = [r["region_id"] for r in regions if r["region_level"] == level]
        if sorted(actual) != sorted(expected):
            raise ValueError(f"ID GeoJSON berbeda dari tabel: {level}")
        ds = None
        tmp.replace(OUT / name)
        result[level] = {"path": name, "id_field": id_field, "feature_count": len(actual)}
    return result


def package_raster():
    reference = gdal.Open(str(ROOT / "data/processed/phase4_change_overview_300m.tif"))
    tiles = sorted((ROOT / "data/interim/phase5/pair_tiles").glob("tile_*.tif"))
    if len(tiles) != 30:
        raise ValueError(f"Harus ada 30 ubin kelas berpasangan. Ditemukan {len(tiles)}.")
    vrt = gdal.BuildVRT("", [str(tile) for tile in tiles],
                        srcNodata=NODATA, VRTNodata=NODATA)
    if (vrt.RasterXSize, vrt.RasterYSize) != (reference.RasterXSize, reference.RasterYSize):
        raise ValueError("Dimensi pasangan kelas tidak sama dengan raster tinjauan fase 4.")
    if not np.allclose(vrt.GetGeoTransform(), reference.GetGeoTransform(), atol=1e-10, rtol=0):
        raise ValueError("Grid pasangan kelas berbeda dari raster tinjauan fase 4.")
    pairs = vrt.ReadAsArray()
    inside = pairs != NODATA
    before, after = pairs // 100, pairs % 100
    if not np.isin(before[inside], [0, *CODES]).all() or not np.isin(after[inside], [0, *CODES]).all():
        raise ValueError("Raster mengandung kode kelas di luar kontrak.")
    change = np.where(inside, np.where((before == 0) | (after == 0), 2, before != after), 255)
    differences = int(np.count_nonzero(change != reference.ReadAsArray()))
    if differences:
        raise ValueError(f"Perubahan yang didekode berbeda pada {differences} piksel.")
    path = "class_pair_2010_2024.tif"
    tmp = OUT / "class_pair.part.tif"
    cog = gdal.Translate(str(tmp), vrt, format="COG", outputType=gdal.GDT_UInt16,
                         noData=NODATA, creationOptions=[
                             "COMPRESS=DEFLATE", "BLOCKSIZE=256", "OVERVIEW_RESAMPLING=NEAREST",
                         ])
    if cog is None:
        raise RuntimeError("Pembuatan COG gagal.")
    cog = None
    cog = gdal.Open(str(tmp))
    if (cog.GetMetadataItem("LAYOUT", "IMAGE_STRUCTURE") != "COG"
        or cog.GetRasterBand(1).GetNoDataValue() != NODATA
        or cog.GetRasterBand(1).GetOverviewCount() < 1
        or not np.array_equal(cog.ReadAsArray(), pairs)):
        raise ValueError("COG hasil gagal diverifikasi.")
    result = {
        "path": path, "format": "COG", "crs": "EPSG:4326",
        "dimensions": [cog.RasterXSize, cog.RasterYSize],
        "geotransform_gdal": list(cog.GetGeoTransform()),
        "overview_count": cog.GetRasterBand(1).GetOverviewCount(),
        "display_pixel_spacing_m_nominal": 300, "analysis_pixel_spacing_m_nominal": 30,
        "nodata_outside_aoi": NODATA, "invalid_class": 0,
        "encoding": "100 * class_2010 + class_2024",
        "decoded_change_mismatch_pixels": differences,
    }
    cog = None
    tmp.replace(OUT / path)
    return result


def main():
    gdal.UseExceptions()
    OUT.mkdir(parents=True, exist_ok=True)
    regions = package_stats()
    boundaries = package_boundaries(regions)
    raster = package_raster()
    qa = json.loads((ROOT / "data/metadata/phase4_qa.json").read_text(encoding="utf-8"))
    manifest = {
        "schema_version": 1, "release": "R1", "years": YEARS,
        "default_region_id": "KALIMANTAN_ID", "default_year": 2024,
        "region_index": regions, "boundaries": boundaries,
        "boundary_display_simplification_degrees": 0.001,
        "raster": raster, "class_order": CODES,
        "classes": [{"code": c, "label": LEGEND[c][0], "color": LEGEND[c][1]} for c in CODES],
        "change_legend": [
            {"code": 0, "label": "Stabil", "color": "#2b8c63"},
            {"code": 1, "label": "Berubah kelas", "color": "#e1842f"},
            {"code": 2, "label": "Tidak dapat dibandingkan", "color": "#747b86"},
        ],
        "statistics": {
            "area_unit": "ha", "annual_denominator": "valid area of the selected year",
            "transition_denominator": "valid area in both years",
            "aoi_method": "direct reduction", "province_method": "sum of districts",
            "district_sum_minus_aoi_ha": qa["district_sum_minus_aoi_ha"],
        },
        "sources": {
            "mapbiomas_asset": CONFIG["mapbiomas"]["asset_id"],
            "mapbiomas_legend": "https://landy.mapbiomas.id/en/legendcode",
            "mapbiomas_license": "CC-BY-SA per provider; license version not stated",
            "mapbiomas_collection": "collection4, internal version v2; 4.1 unconfirmed",
            "boundaries": CONFIG["region"]["boundary_version"],
            "boundary_completeness_verified": False,
            "boundary_distribution_terms_verified": False,
        },
        "publication_status": "local integration only; review boundary distribution terms before publication",
    }
    write_json(OUT / "manifest.json", manifest)
    print(json.dumps({"region_count": len(regions), "raster": raster,
                      "bytes": {p.name: p.stat().st_size for p in OUT.iterdir() if p.is_file()}},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
