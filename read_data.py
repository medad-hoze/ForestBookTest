

import pandas as pd
import numpy as np

from arcgis.gis import GIS


org          = 'https://kkl.maps.arcgis.com/home'
agoluser     = 'medadhozekkl'
agolpwd      = 'medadhozekkl123'
gis          = GIS(url=org, username=agoluser, password=agolpwd,timeout=5000)


id_path = '99791b9d4dde4de3b1b6974ac82b81af'

item_path = gis.content.get(id_path)

df_path = item_path.layers[0].query(where='1=1', out_fields='*', return_geometry=True).sdf



push_test = '0d6e6c8ba1c1497aa361342dc37e92b7'



df_2 = df_path.head(200)

df_2.to_excel('test_path.xlsx', index=False)


####
# 1. check field columns as test
# 2. create centrel point connected with global id and parent global id
# 3. copy the global id from the point and pass to the table


# duplicat F_H_P

duplicated_F_H_P = df_path.groupby('F_H_P').filter(lambda x: len(x) > 1)

uni = df_path.drop_duplicates(subset=['F_H_P'])



df_path.to_excel('test_path_full.xlsx', index=False)