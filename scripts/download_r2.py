"""Download the 15-year display stack on the existing R1 overview grid."""

import json
from concurrent.futures import ThreadPoolExecutor

import ee
import requests

from prepare_phase3_rasters import CONFIG, CODES, CRS, GRID, PROJECT, ROOT
from analyze_r2 import YEARS


def main():
    ee.Initialize(project=PROJECT)
    ee.data.setDeadline(280000)
    report = json.loads((ROOT / "data/metadata/r2_audit.json").read_text())
    folder = ROOT / "data/interim/r2" / report["cache_key"] / "tiles"
    folder.mkdir(parents=True, exist_ok=True)
    reference = json.loads((ROOT / "web/public/data/r1/manifest.json").read_text())["raster"]
    width, height = reference["dimensions"]
    west, dx, _, north, _, dy = reference["geotransform_gdal"]
    source = ee.Image(CONFIG["mapbiomas"]["asset_id"])
    boundary = ee.FeatureCollection(CONFIG["region"]["boundary_asset_id"])
    stack = ee.Image.cat(*[source.select(f"classification_{y}").remap(CODES, CODES, 0)
                         .unmask(0, False).rename(f"class_{y}") for y in YEARS]).toByte()

    def download(tile):
        x, y = tile
        target = folder / f"tile_{y}_{x}.tif"
        if target.exists():
            return
        w, h = min(768, width - x), min(768, height - y)
        lon, lat = west + x * dx, north + y * dy
        footprint = ee.Geometry.Rectangle([lon - GRID[0], lat + h * dy + GRID[4],
                                           lon + w * dx + GRID[0], lat - GRID[4]], geodesic=False)
        image = stack.clipToCollection(boundary.filterBounds(footprint)).unmask(255, False)
        url = image.getDownloadURL({"crs": CRS, "crs_transform": [dx, 0, lon, 0, dy, lat],
                                   "dimensions": [w, h], "format": "GEO_TIFF", "filePerBand": False})
        response = requests.get(url, timeout=180)
        if not response.ok or response.content[:4] not in (b"II*\x00", b"MM\x00*"):
            raise RuntimeError(f"Unduhan raster gagal {x},{y}, HTTP {response.status_code}")
        temporary = target.with_suffix(".part")
        temporary.write_bytes(response.content)
        temporary.replace(target)
        print(f"Raster 15 tahun siap {x},{y}", flush=True)

    tiles = [(x, y) for y in range(0, height, 768) for x in range(0, width, 768)]
    with ThreadPoolExecutor(max_workers=2) as pool:
        list(pool.map(download, tiles))


if __name__ == "__main__":
    main()
