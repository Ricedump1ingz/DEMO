import folium
import pandas as pd
import geopandas as gpd
import branca
import branca.colormap as cm
import os
import sys
os.environ['PROJ_LIB'] = os.path.dirname(sys.argv[0])

def single():
    #读取轨迹文件
    straj = gpd.read_file('data/straj2.gpkg')
    #O点和D点
    ori = gpd.read_file('data/ori2.gpkg')
    des = gpd.read_file('data/des2.gpkg')
    #订单信息以及各参数
    orders = pd.read_csv('data/share_map.csv',sep = ',')

    def subtable(order2):
        sub = order2.iloc[0]
        left_col_colour = "#2A799C"
        right_col_colour = "#C5DCE7"
        ID = sub['driverID']
        time = sub['trip_time']/60
        distance = sub['trip_distance']
        OR = sub['OR']
        detour = sub['detour_rate']
        proba = sub['proba']
        html = """<!DOCTYPE html>
        <html>

        <head>
        <h4 style="margin-bottom:0"; width="300px">{}</h4>""".format('合乘代码：<br>'+ID) + """

        </head>
            <table style="height: 126px; width: 300px;">
        <tbody>
        <tr>
        <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">行程时间（min）</span></td>
        <td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(time) + """
        </tr>
        <tr>
        <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">总距离（km）</span></td>
        <td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(distance) + """
        </tr>
        <tr>
        <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">重叠率</span></td>
        <td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(OR) + """
        </tr>
        <tr>
        <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">绕路比</span></td>
        <td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(detour) + """
        </tr>
        <tr>
        <td style="background-color: """+ left_col_colour +""";"><span style="color: #ffffff;">减排概率</span></td>
        <td style="width: 200px;background-color: """+ right_col_colour +""";">{}</td>""".format(proba) + """
        </tr>
        </tbody>
        </table>
        </html>
        """
        return html

    m3 = folium.Map(zoom_start=10,
                    tiles='http://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetGray/MapServer/tile/{z}/{y}/{x}',
                    attr= '灰色版',
                    max_bounds=True)
    folium.map.FitBounds([(30.65,104.04),(30.72,104.12)], padding_top_left=None, padding_bottom_right=None, padding=None, max_zoom=None).add_to(m3)
    colormap = cm.LinearColormap(colors=['red','orange','yellow','green','blue','purple'], vmin=0,vmax=7)
    one = straj.sample( n = 1)
    for row in one.itertuples():
         #提取x，y并反向，因为folium里用的是y，x
        x,y = row.geometry.coords.xy
        loc = list(zip(y,x))
        driver = row[1]
        order2 = orders.loc[orders['driverID'] == row[1]]
        ind = orders.loc[orders['driverID'] == row[1]].index[0]
        tool = folium.map.Tooltip('行程时间：%d分钟<br>重叠率：%.2f<br>绕路比：%.2f<br>减排概率：%.2f'%(order2['trip_time']/60,order2['OR'],order2['detour_rate'],order2['proba']))
        col = colormap(ind)
        html = subtable(order2)
        iframe = branca.element.IFrame(html=html,width=350,height=250)
        popup = folium.Popup(iframe,parse_html=True)
        folium.PolyLine(loc,color=col,weight=5,opacity=0.75,tooltip = tool, popup = popup).add_to(m3)
    new_ori = ori.loc[ori['driverID'] == driver]
    o1 = new_ori.iloc[0]
    folium.Marker(
                        location=[o1[5], o1[4]],
                        popup=('订单号:\n%s'%o1[1]),
                        icon=folium.Icon(color='blue'),
                        ).add_to(m3)
    folium.Marker(
                        location=[o1[7], o1[6]],
                        popup=('订单号:\n%s'%o1[1]),
                        icon=folium.Icon(color='blue', icon='home'),
                        ).add_to(m3)
    o2 = new_ori.iloc[1]
    folium.Marker(
                        location=[o2[5], o2[4]],
                        popup=('订单号:\n%s'%o2[1]),
                        icon=folium.Icon(color='orange'),
                        ).add_to(m3)
    folium.Marker(
                        location=[o2[7], o2[6]],
                        popup=('订单号:\n%s'%o2[1]),
                        icon=folium.Icon(color='orange', icon='home'),
                        ).add_to(m3)
    return m3
