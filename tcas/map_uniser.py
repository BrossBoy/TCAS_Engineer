import pandas as pd
import json
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import numpy as np

# Load JSON data
with open('data/univer_lat_long.json', encoding="utf-8") as json_file:
    geo_json = json.load(json_file)

uni_list = []
dropdown = []

# JSON to dataframe
for i in geo_json:        
    uni_list.append([i, geo_json[i]['lat'], geo_json[i]['long']])
    dropdown.append({'label': i, 'value': i})  # Dropdown options need to be dictionaries
df = pd.DataFrame(uni_list, columns=['name', 'lat', 'lon'])

mapbox_access_token = 'pk.eyJ1IjoiYW51d2F0ayIsImEiOiJjbHo1YXNkNjAxZnA4MnFwc25hMXFzc3gyIn0.26H6V6Uf6DJeWUOS0Rb0Cw'

app = Dash(__name__)
app.layout = html.Div([
    html.H1(children='Tcas Dashboard'),
    dcc.Dropdown(id='dropdown', placeholder='ชื่อมหาวิทยาลัย', options=dropdown),
    dcc.Graph(id='map')
])

@app.callback(
    Output("map", "figure"),
    Input("dropdown", "value"),
)
def display_scatter(dropdown):
    data = df
    map_zoom = 7
    if dropdown is not None:
        data = df[df['name'] == dropdown]
        map_zoom = 10

    # Create the Scattermapbox plot
    fig = go.Figure(go.Scattermapbox(
        mode="markers",
        lon=data['lon'], lat=data['lat'],
        marker={
            'size': 20, 
            'symbol': "college",  # Change to "marker" symbol for location marker
            'color': "Crimson"  # Optional: change color to distinguish the markers
        },
        text=data['name'],
        textposition="bottom right"
    ))
    
    fig.update_layout(
        autosize=True,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            style='mapbox://styles/mapbox/streets-v11',
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=np.mean(data['lat']),
                lon=np.mean(data['lon'])
            ),
            pitch=0,
            zoom=map_zoom
        ),
        margin={"r":0, "t":0, "l":0, "b":0}
    )
    
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)


