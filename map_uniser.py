import plotly.express as px
import pandas as pd
import json
from dash import Dash,dcc,html,Input,Output


with open('data/univer_lat_long.json', encoding="utf-8") as json_file:
    geo_json= json.load(json_file)
uni_list =[]
dropdown = []

# json to dataframe
for i in geo_json:        
    uni_list.append([i,geo_json[i]['lat'],geo_json[i]['long']])
    dropdown.append(i)
df = pd.DataFrame(uni_list,columns=['name','lat','lon'])

app = Dash()
app.layout = [
    html.H1(children='Tcas Dashboard'),
    dcc.Dropdown(id='dropdown', placeholder='ชื่อมหาวิทยาลัย', options=dropdown),
    dcc.Graph(id='map')
]

@app.callback(
    Output("map", "figure"),
    Input("dropdown", "value"),
)

def display_scatter(dropdown):
    data = df
    if dropdown != None:
        data = df[df['name']==dropdown]

    #mark university location
    fig = px.scatter_mapbox(data,
                            lat='lat',
                            lon='lon',
                            hover_name="name",
                            hover_data=dict(lat = False,lon = False), #not show latitude and longitude
                            size_max=10,
                            color_discrete_sequence=["DarkBlue"],
                            zoom=7)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig


if __name__=="__main__":
    app.run(debug=True)