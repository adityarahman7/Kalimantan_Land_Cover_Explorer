"""Build the Phase 3 boundary package in the open QGIS project."""

import json
from collections import defaultdict
from pathlib import Path

from qgis.PyQt.QtCore import QVariant
from qgis.core import (
    QgsFeature, QgsField, QgsGeometry, QgsProject,
    QgsVectorFileWriter, QgsVectorLayer, QgsWkbTypes,
)

root = Path(__file__).resolve().parent.parent
live = QgsProject.instance()
source_path = root / "data/interim/batas_admin_gee/batas_admin_kalimantan.shp"
source = QgsVectorLayer(str(source_path), "Batas kerja", "ogr")
if not source.isValid() or source.crs().authid() != "EPSG:4326":
    raise ValueError("Batas kerja harus terbaca dalam EPSG:4326.")

groups = defaultdict(list)
province_names = {}
district_rows = []
district_codes = set()
for feature in source.getFeatures():
    district_id, district_name, province_id, province_name = (
        str(feature[key]).strip() for key in ("KDPKAB", "WADMKK", "KDPPUM", "WADMPR")
    )
    geometry = feature.geometry()
    if (not district_id or district_id in district_codes
        or not district_name or province_id not in {"61", "62", "63", "64", "65"}
        or not province_name or geometry.isEmpty() or not geometry.isGeosValid()):
        raise ValueError(f"Fitur sumber bermasalah: {feature.id()}")
    if province_names.setdefault(province_id, province_name) != province_name:
        raise ValueError(f"Nama provinsi tidak konsisten: {province_id}")
    district_codes.add(district_id)
    groups[province_id].append(geometry)
    district_rows.append((geometry, [district_id, district_name, province_id, province_name]))

if len(district_rows) != 56 or len(groups) != 5:
    raise ValueError("Jumlah atau tingkat batas kerja berbeda dari hasil audit.")

province_rows = []
overlap_within = {}
for province_id, geometries in sorted(groups.items()):
    union = QgsGeometry.unaryUnion(geometries)
    if union.isEmpty() or not union.isGeosValid():
        raise ValueError(f"Dissolve gagal: {province_id}")
    province_rows.append((union, [province_id, province_names[province_id]]))
    overlap_within[province_id] = max(0.0, sum(g.area() for g in geometries) - union.area())

aoi = QgsGeometry.unaryUnion([geometry for geometry, _ in province_rows])
if aoi.isEmpty() or not aoi.isGeosValid():
    raise ValueError("Dissolve AOI gagal.")
overlap_between = max(0.0, sum(g.area() for g, _ in province_rows) - aoi.area())

target = root / "data/processed/phase3_boundaries.gpkg"
if target.exists():
    raise FileExistsError(target)
target.parent.mkdir(parents=True, exist_ok=True)

datasets = [
    ("kabupaten_kota", ["district_id", "district_name", "province_id", "province_name"], district_rows),
    ("provinsi", ["province_id", "province_name"], province_rows),
    ("aoi", ["aoi_id", "aoi_name"], [(aoi, ["KALIMANTAN_ID", "Kalimantan Indonesia"])]),
]

report = {
    "source": source_path.relative_to(root).as_posix(),
    "crs": source.crs().authid(),
    "boundary_scope": "56-feature working extent; source island without district identifier excluded",
    "overlap_within_province_square_degrees": overlap_within,
    "overlap_between_provinces_square_degrees": overlap_between,
    "overlap_method": "max(0, sum of component planar areas minus dissolved planar area); diagnostic only",
    "gap_completeness_verified": False,
    "layers": {},
}
for index, (name, fields, rows) in enumerate(datasets):
    kind = QgsWkbTypes.displayString(rows[0][0].wkbType())
    layer = QgsVectorLayer(kind + "?crs=EPSG:4326", name, "memory")
    provider = layer.dataProvider()
    provider.addAttributes([QgsField(field, QVariant.String) for field in fields])
    layer.updateFields()
    features = []
    for geometry, attributes in rows:
        feature = QgsFeature(layer.fields())
        feature.setGeometry(geometry)
        feature.setAttributes(attributes)
        features.append(feature)
    if not provider.addFeatures(features)[0]:
        raise RuntimeError(f"Gagal membuat layer {name}")
    options = QgsVectorFileWriter.SaveVectorOptions()
    options.driverName = "GPKG"
    options.layerName = name
    if index:
        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
    result = QgsVectorFileWriter.writeAsVectorFormatV3(
        layer, str(target), live.transformContext(), options
    )
    if result[0] != QgsVectorFileWriter.NoError:
        raise RuntimeError(result)
    output = QgsVectorLayer(f"{target}|layername={name}", name, "ogr")
    saved = list(output.getFeatures())
    if (not output.isValid() or output.crs().authid() != "EPSG:4326"
        or len(saved) != len(rows)
        or any(f.geometry().isEmpty() or not f.geometry().isGeosValid() for f in saved)
        or sorted(tuple(str(f[key]) for key in fields) for f in saved)
        != sorted(tuple(attributes) for _, attributes in rows)):
        raise RuntimeError(f"Pemeriksaan pembukaan ulang gagal: {name}")
    report["layers"][name] = {"feature_count": len(saved), "valid_geometries": len(saved), "fields": fields}

report["layers_reopened"] = True
report_path = root / "data/metadata/phase3_boundary_qa.json"
report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, ensure_ascii=False))
