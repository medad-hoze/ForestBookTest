



import pandas as pd

from arcgis.gis import GIS
import os
import ssl,datetime
from sqlalchemy import create_engine,text,inspect
from tqdm import tqdm

from arcgis.gis       import GIS
from datetime         import datetime, timedelta
from shapely.geometry import Point

from tqdm import tqdm


################################################################################

org          = 'https://kkl.maps.arcgis.com/home'
agoluser     = 'medadhozekkl'
agolpwd      = 'medadhozekkl123'
gis          = GIS(url=org, username=agoluser, password=agolpwd,timeout=5000)

################################################################################

user      = 'postgres'
password  = '1515'
host      = 'localhost'
port      = '5432'
database  = 'postgres' 


engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')


################################################################################


def to_wkt(geom):
    if geom is None:
        return None
    return Point(geom["x"], geom["y"]).wkt



item_id = '0d6e6c8ba1c1497aa361342dc37e92b7'
treeStoryDetails = gis.content.get(item_id)


point_agol = treeStoryDetails.layers[1]
df_point = point_agol.query(where='1=1', out_fields='*', return_geometry=True).sdf


out             = df_point.copy()
out["geometry"] = out["SHAPE"].apply(to_wkt)


bad_cols = []
for c in out.columns:
    if out[c].dtype == "object":
        sample = next((v for v in out[c].head(50).tolist() if v is not None), None)
        if isinstance(sample, (dict, list)) or sample.__class__.__name__ in ("Point","Polygon","LineString"):
            bad_cols.append(c)

if "SHAPE" in out.columns and "SHAPE" not in bad_cols:
    bad_cols.append("SHAPE")

out = out.drop(columns=bad_cols)

# get to .geojson

import geopandas as gpd
from shapely.wkt import loads as wkt_loads

if out['geometry'].dtype == 'object' and isinstance(out['geometry'].iloc[0], str):
    out['geometry'] = out['geometry'].apply(wkt_loads)

gdf = gpd.GeoDataFrame(out, geometry='geometry', crs="EPSG:2039")  # set your CRS


gdf.to_file("point_agol.geojson", driver="GeoJSON")

# out.to_sql("forestBook", engine, if_exists="replace", index=False)
