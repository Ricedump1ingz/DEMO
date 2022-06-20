import folium
import pandas as pd
import geopandas as gpd
import branca
import branca.colormap as cm

import os
import sys
os.environ['PROJ_LIB'] = os.path.dirname(sys.argv[0])

def origin():
    ori = gpd.read_file('D:/Files/2020交通科技大赛/demo/ori2.gpkg')
    m2 = folium.Map(zoom_start=10,
                    tiles='http://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetGray/MapServer/tile/{z}/{y}/{x}',
                    attr= '灰色版',
                    max_bounds=True)
    folium.map.FitBounds([(30.65,104.04),(30.72,104.12)], padding_top_left=None, padding_bottom_right=None, padding=None, max_zoom=None).add_to(m2)
    for row in ori.itertuples():
        folium.Marker(
                        location=[row[6], row[5]],
                        popup=('订单号:\n%s'%row[2]),
                        icon=folium.Icon(color='blue'),
                        ).add_to(m2)
    return m2