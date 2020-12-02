import folium # Folium is a Python library used for visualizing geospatial data.  Folium is a Python wrapper for Leaflet. js which is a leading open-source JavaScript library for plotting interactive maps.
import pandas

map = folium.Map # defining a map object
map = folium.Map(location = [38.85 , -99.09] , zoom_start=6 , tiles = "Stamen Terrain")   # default values shown when map is opened

# Add a marker
#map.add_child (folium.Marker (location = [38.2 , -99.1] , popup= "Hi I am a marker" , icon = folium.Icon(color = 'green') ))

# Instead of above code you can use "FeatureGroup" as below: (for exampe "Marker" is a group)
fgv= folium.FeatureGroup (name = "Volcanoes")

#reading markers from file
data=pandas.read_csv("Volcanoes.txt" )
lat= list (data["LAT"])
lon= list (data["LON"])
elev= list (data["ELEV"])
name = list(data["NAME"])

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000<=elevation <3000:
        return 'orange'
    else:
        return 'red'


##----Version#1 of popup----- ##if you want to have stylized text (bold, different fonts, etc) in the popup window you can use HTML:
#html = """<h4>Volcano information:</h4> Height: %s m"""

##----Version#2 of popup-------
#You can even put links in the popup window. For example, the code below will produce a popup window with the name of the volcano as a link which does a Google search for that particular volcano when clicked:
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""


# adding markers
for lt , ln , el ,name in zip (lat,lon , elev ,name ): # zip () function distributes items 1by1
    #fg.add_child (folium.Marker (location = [lt , ln] , popup=str(el) + "m" , icon = folium.Icon(color = 'green') )) 
    #instead of above code, if you want to have stylized text (bold, different fonts, etc) in the popup window you can use HTML:
    
    #iframe = folium.IFrame(html=html % str(el), width=200, height=100) #----Version#1 of popup-----
    iframe = folium.IFrame(html=html % (name , name, el), width=200, height=100) #----Version#2 of popup-----

    #fg.add_child (folium.Marker (location = [lt , ln] , popup=folium.Popup(iframe) , icon = folium.Icon(color = "green") )) #----Version#3: adding color to marker-----
    #fg.add_child (folium.Marker (location = [lt , ln] , popup=folium.Popup(iframe) , icon = folium.Icon(color = color_producer(el)  ) ))  # #----Version#4: adding dynamic colors to marker----- 

    # use Circle instead of marker
    fgv.add_child (folium.CircleMarker (location = [lt , ln] , popup=folium.Popup(iframe) , raduis = 6   , fill_color=color_producer(el) , color='grey'  , fill_opacity=0.7 )) 

    

#adding a GeoJson Polygon layer
fgp = folium.FeatureGroup (name = "Population")
fgp.add_child (folium.GeoJson(data=  open('world.json' , 'r' , encoding = 'utf-8-sig').read()  ,
style_function = lambda x: {'fillColor' : 'green'  if x['properties'] ['POP2005'] < 1000000  
else 'orange'  if 10000000 <= x['properties'] ['POP2005'] <50000000 else 'red'} ) ) # Draws blue polygons around conutries


#finally
map.add_child (fgv) 
map.add_child (fgp)


#layer control  (This way you could remove a layer if you want ). You need to add this line afte previous line: map.add_child (fg)
#once you add layerControl you will see a button on right top corner of the map
map.add_child(folium.LayerControl())

map.save ("Map.html")



