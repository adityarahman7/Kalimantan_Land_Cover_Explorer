"""Assemble and verify the Phase 4 display overview inside QGIS."""

import json
import math
from collections import Counter
from pathlib import Path

import numpy as np
from osgeo import gdal
from qgis.PyQt.QtGui import QColor
from qgis.core import QgsPalettedRasterRenderer, QgsProject, QgsRasterLayer

root = Path(__file__).resolve().parent.parent
config = json.loads((root / "config/project.example.json").read_text(encoding="utf-8"))
grid = config["analysis"]["crs_transform"]
dx, dy = grid[0] * 10, grid[4] * 10
west, south, east, north = 108.59, -4.95, 119.04, 4.42
left = math.floor((west - grid[2]) / dx)
right = math.ceil((east - grid[2]) / dx)
top = math.floor((north - grid[5]) / dy)
bottom = math.ceil((south - grid[5]) / dy)
tile_size = 768
tiles = []
counts = Counter()
for y in range(top, bottom, tile_size):
    for x in range(left, right, tile_size):
        path = root / f"data/interim/phase4/overview_tiles/tile_{y}_{x}.tif"
        ds = gdal.Open(str(path))
        if ds is None:
            raise ValueError(f"Ubin tidak dapat dibuka: {path}")
        transform = (grid[2] + x * dx, dx, 0, grid[5] + y * dy, 0, dy)
        if (ds.RasterXSize != min(tile_size, right-x)
            or ds.RasterYSize != min(tile_size, bottom-y)
            or ds.RasterCount != 1 or ds.GetSpatialRef().GetAuthorityCode(None) != "4326"
            or any(abs(a-b) > 1e-10 for a, b in zip(ds.GetGeoTransform(), transform, strict=True))):
            raise ValueError(f"Grid, ukuran, atau CRS ubin berbeda: {path}")
        values, n = np.unique(ds.ReadAsArray(), return_counts=True)
        counts.update({int(k): int(v) for k, v in zip(values, n, strict=True)})
        ds = None
        tiles.append(str(path))
if set(counts) != {0, 1, 2, 255} or sum(counts.values()) != (right-left) * (bottom-top):
    raise ValueError(f"Kode atau jumlah piksel tinjauan tidak sesuai: {counts}")

target = root / "data/processed/phase4_change_overview_300m.tif"
if not target.exists():
    vrt = gdal.BuildVRT("", tiles, srcNodata=255, VRTNodata=255)
    tmp = target.with_name("phase4_change_overview_300m.part.tif")
    merged = gdal.Translate(str(tmp), vrt, format="GTiff",
                            creationOptions=["TILED=YES", "COMPRESS=DEFLATE"])
    if merged is None:
        raise RuntimeError("Mosaik tidak berhasil dibuat.")
    merged.GetRasterBand(1).SetDescription("change_2010_2024")
    merged = None
    vrt = None
    tmp.replace(target)
merged = gdal.Open(str(target))
if merged is None or (merged.RasterXSize, merged.RasterYSize) != (right-left, bottom-top):
    raise RuntimeError("Ukuran mosaik tidak sesuai grid tinjauan.")
values, n = np.unique(merged.ReadAsArray(), return_counts=True)
if dict(zip(map(int, values), map(int, n), strict=True)) != counts:
    raise RuntimeError("Jumlah piksel mosaik berbeda dari jumlah ubin.")
merged = None

project_path = root / "Kalimantan_Land_Cover_Explorer.qgz"
project = QgsProject()
if not project.read(str(project_path)):
    raise RuntimeError("Proyek utama tidak dapat dibuka.")
layer = QgsRasterLayer(str(target), "Perubahan 2010–2024 | tinjauan 300 m", "gdal")
if not layer.isValid():
    raise RuntimeError("Raster hasil tidak dapat dibuka di QGIS.")
layer.setRenderer(QgsPalettedRasterRenderer(layer.dataProvider(), 1, [
    QgsPalettedRasterRenderer.Class(0, QColor("#2b8c63"), "Stabil"),
    QgsPalettedRasterRenderer.Class(1, QColor("#e1842f"), "Berubah kelas"),
    QgsPalettedRasterRenderer.Class(2, QColor("#747b86"), "Tidak dapat dibandingkan"),
]))
if not any(Path(item.source()) == target for item in project.mapLayers().values()
           if isinstance(item, QgsRasterLayer)):
    project.addMapLayer(layer, False)
    tree = project.layerTreeRoot()
    group = tree.findGroup("Fase 4 - analisis perubahan") or tree.addGroup("Fase 4 - analisis perubahan")
    group.addLayer(layer).setItemVisibilityChecked(False)
    if not project.write():
        raise RuntimeError(f"Penyimpanan proyek utama gagal: {project.error()}")
check = QgsProject()
if (not check.read(str(project_path)) or len(check.mapLayers()) != len(project.mapLayers())
    or any(not item.isValid() for item in check.mapLayers().values())):
    raise RuntimeError("Proyek fase 4 gagal dibuka ulang.")

qa_path = root / "data/metadata/phase4_qa.json"
qa = json.loads(qa_path.read_text(encoding="utf-8"))
qa["overview"] = {
    "role": "categorical display overview at 10x native pixel spacing; not used for area statistics",
    "path": target.relative_to(root).as_posix(),
    "crs": "EPSG:4326",
    "dimensions": [right-left, bottom-top],
    "tiles": len(tiles),
    "pixel_counts_display_only": dict(sorted(counts.items())),
    "qgis_project": project_path.name,
    "qgis_reopened": True,
}
qa_path.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(qa["overview"], ensure_ascii=False))
