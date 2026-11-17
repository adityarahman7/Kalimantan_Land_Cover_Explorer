import json
from pathlib import Path
from osgeo import ogr
root = Path(__file__).resolve().parents[1]
source = root / 'data/interim/ne_10m_land.geojson'
out = root / 'web/public/context'
out.mkdir(parents=True, exist_ok=True)
clip = ogr.CreateGeometryFromWkt('POLYGON ((85 -20,145 -20,145 25,85 25,85 -20))')
data = json.loads(source.read_text(encoding='utf-8'))
features = []
for feature in data['features']:
    geom = ogr.CreateGeometryFromJson(json.dumps(feature['geometry']))
    cropped = geom.Intersection(clip)
    if not cropped.IsEmpty():
        simplified = cropped.SimplifyPreserveTopology(0.002)
        features.append({'type':'Feature','properties':{},'geometry':json.loads(simplified.ExportToJson())})
result = {'type':'FeatureCollection','features':features}
(out / 'regional-land.geojson').write_text(json.dumps(result,separators=(',',':')),encoding='utf-8')
metadata = {'source':'Natural Earth ne_10m_land','source_url':'https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_land.geojson','license':'Public domain','license_url':'https://www.naturalearthdata.com/about/terms-of-use/','downloaded_on':'2026-11-17','source_scale':'1:10,000,000 (not 10-metre resolution)','bbox':[85,-20,145,25],'simplification_degrees':0.002,'purpose':'Regional coastline context only; not administrative boundaries or an analysis input.'}
(out / 'source.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
print(len(features), (out / 'regional-land.geojson').stat().st_size)
