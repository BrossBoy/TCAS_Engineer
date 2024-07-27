import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json


with open('data/univer_lat_long.json', encoding="utf-8") as json_file:
    geo_json= json.load(json_file)


uni_list =[]



# print(geo_json)
for i in geo_json:
    uni_list.append([i,geo_json[i]['lat'],geo_json[i]['long']])
df = pd.DataFrame(uni_list,columns=['name','lat','lon'])
fig = px.scatter_mapbox(df,
                        lat='lat',
                        lon='lon',
                        hover_name="name",
                        hover_data=dict(lat = False,lon = False), #not show latitude and longitude
                        size_max=10,
                        color_discrete_sequence=["DarkBlue"],
                        zoom=1)
fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.show()
