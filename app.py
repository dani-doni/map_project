from flask import Flask, render_template_string

import folium
from folium import plugins
from urllib.request import urlopen
import json
import pandas as pd

app = Flask(__name__)

@app.route("/")
def fullscreen():
    # Create the map with centrum in Gottolengo
    my_map= folium.Map(location=[45.2928, 10.2734])
    # add searching bar
    plugins.Geocoder().add_to(my_map)
    # Add custom base maps to folium
    basemaps = {
        'Google Maps': folium.TileLayer(
            tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
            attr = 'Google',
            name = 'Google Maps',
            overlay = True,
            control = True
        ),
        'Google Satellite': folium.TileLayer(
            tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
            attr = 'Google',
            name = 'Google Satellite',
            overlay = True,
            control = True
        ),
        'Google Satellite Hybrid': folium.TileLayer(
            tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
            attr = 'Google',
            name = 'Google Satellite',
            overlay = True,
            control = True
        )
    }

    # Add custom basemaps
    basemaps['Google Maps'].add_to(my_map)
    basemaps['Google Satellite'].add_to(my_map)
    basemaps['Google Satellite Hybrid'].add_to(my_map)

    # Add a layer control panel to the map.
    my_map.add_child(folium.LayerControl())
    #fullscreen
    plugins.Fullscreen().add_to(my_map)
    #GPS
    plugins.LocateControl().add_to(my_map)
    #mouse position
    fmtr = "function(num) {return L.Util.formatNum(num, 3) + ' º ';};"
    plugins.MousePosition(position='topright', separator=' | ', prefix="Mouse:",lat_formatter=fmtr, lng_formatter=fmtr).add_to(my_map)
    #Add the draw 
    plugins.Draw(export=True, filename='data.geojson', position='topleft', draw_options=None, edit_options=None).add_to(my_map)  
    #Add measure tool 
    plugins.MeasureControl(position='topright', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(my_map)

    # store the URL in url as 
    # parameter for urlopen
    url = "https://raw.githubusercontent.com/dani-doni/immobiliare/main/gottolengo_compravendite.json"
  
    # store the response of URL
    response = urlopen(url)
  
    # storing the JSON response 
    # from url in data
    data_json = json.loads(response.read())
    data = data_json['data']
    results = data['result']
    for i in range(0,len(results)):
        immobili = results[i]
        imm_det = immobili['immobili']
        particella = imm_det[0]
        location_points = particella['location_point']
        coordinates = location_points['coordinates']
        columns = ["#","CODCAT", "dizione", "indirizzo"]
        table_head = f"<thead>\n<tr><th>{'</th><th>'.join(columns)}</th></tr>\n</thead>"
        table_body = "\n<tbody>\n"
        for j in range(0,immobili['totale_immobili']):
            try:
              particella = imm_det[j]
              part_data = [f"{i}.",particella['CODCAT'],particella['dizione'],particella['indirizzo']]
              table_body += f"<tr><td>{'</td><td>'.join(part_data)}</td></tr>\n"
            except:
              pass
        table_body += "</tbody>\n"
        html = f"<table>\n{table_head}{table_body}</table>"
        iframe = folium.IFrame(html=html, width=500, height=500)
        popup = folium.Popup(iframe, max_width=1650)
        folium.Marker(
          location=[coordinates[0],coordinates[1]],
          popup=popup,
          icon=folium.Icon(icon='home', prefix='fa')
        ).add_to(my_map)
        
    return my_map.get_root().render()



