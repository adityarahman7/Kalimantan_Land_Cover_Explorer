"""Create the browser's lossless R1 raster from the verified Phase 5 COG."""

import gzip
import json
from pathlib import Path

from osgeo import gdal


DATA = Path(__file__).resolve().parents[1] / "web/public/data/r1"


def main():
    gdal.UseExceptions()
    manifest = json.loads((DATA / "manifest.json").read_text(encoding="utf-8"))
    raster = manifest["raster"]
    source = gdal.Open(str(DATA / raster["path"]))
    if ([source.RasterXSize, source.RasterYSize] != raster["dimensions"]
            or list(source.GetGeoTransform()) != raster["geotransform_gdal"]
            or source.GetRasterBand(1).DataType != gdal.GDT_UInt16):
        raise ValueError("Raster sumber berbeda dari kontrak manifest R1.")
    raw = source.ReadAsArray().astype("<u2", copy=False).tobytes()
    packed = gzip.compress(raw, compresslevel=6, mtime=0)
    temp = DATA / "class_pair.part"
    temp.write_bytes(packed)
    temp.replace(DATA / "class_pair_2010_2024.u16.gz")
    print(f"{source.RasterXSize} x {source.RasterYSize} | {len(packed):,} byte")


if __name__ == "__main__":
    main()
