import folium
import pandas
from folium.map import FeatureGroup, Icon, Popup

volcanoes = pandas.read_csv("Volcanoes.txt")

latitude = list(volcanoes["LAT"])
longtitude = list(volcanoes["LON"])
elevation = list(volcanoes["ELEV"])
name = list(volcanoes["NAME"])


html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank" style="color: black"><b>%s</b></a><br>
Height: %s m
"""

def color_Detection(e):
    if e < 1000:
        return "green"
    elif e >= 1000 and e <=3000:
        return "orange"
    else:
        return "red"

map = folium.Map(location=[22.466937700597764, 72.74556402630014], zoom_start=2, tiles='Stamen Terrain')

fgv = FeatureGroup(name="Volcanoes")

for lat, lon, elv, name in zip(latitude, longtitude, elevation, name):
    iframe = folium.IFrame(html=html % (name, name, elv), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lat, lon], popup=folium.Popup(iframe), radius=8, fill_color= color_Detection(elv), color ='black', fill_opacity=0.7, icon=folium.Icon(color=color_Detection(elv))))

fgp = FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open("world.json", "r", encoding="utf-8-sig").read(), 
style_function=lambda x: {"fillColor" : "green" if x['properties']['POP2005'] < 10000000 
else 'yellow' if 1000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))


map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl(collapsed=False))
map.save("map1.html")


