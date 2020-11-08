import dash_core_components as dcc
import dash_html_components as html

from urllib.request import urlopen

import json
import pandas as pd
import plotly.express as px
from datetime import date
import dash_table
import numpy as np
import plotly.graph_objects as go
from data_load.utils import line_info
from data_load.loader import BigLineLoader
from data_load.loader import LineLoader, ConstructionSiteLoader
from data_load.trouble_management import TroubleManager

d = BigLineLoader().set_sort_km().load()
d = d.rename(columns={'latitude': 'lat', 'longitude': 'lon'})
d['line_group'] = d['linie']
d['color'] = ['green'] * len(d)
print(d)

fig = px.line_mapbox(d, lat="lat", lon="lon", hover_name="bezeichnung_bps", hover_data=["linienname", "linie"],
                        line_group='line_group', color='color')
fig.update_layout(
    mapbox_zoom=6,  # hardcoded values for center of switzerland, can be adjusted automagically when we have the data
    mapbox_center_lat=46.87,
    mapbox_center_lon=8.13,
    mapbox_style="white-bg",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "source": [
                "http://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png"
            ]
        }
    ])
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


'''
for i, line in enumerate(line_info(d)):
    line_dict = dict(mode="markers+lines",
                     lon=line['lon'],
                     lat=line['lat'],
                     marker={'size': 10})
    if len(line['lon']) > 2:
        fig.add_trace(**line_dict) #go.Scattermapbox(**line_dict))
'''

line_data = LineLoader().load()
construction_data = ConstructionSiteLoader().load()
troubleLoader = TroubleManager(construction_data, line_data)
troubleLoader.filter_by_time(date(2020, 7, 11),date(2025,7,11))
df = troubleLoader.working_dataset.loc[:,["bp_to","bp_from","reduction_capacity","date_to","date_from"]]



def main_structure():
    return html.Div([
        html.Div([
            dcc.DatePickerRange(
                id='date-range-graphic',
                min_date_allowed=date(2020, 7, 11),
                max_date_allowed=date(2050, 7, 11),
                initial_visible_month=date(2020, 7, 11),
                start_date=date(2020, 7, 11),
                end_date=date(2021, 7, 11),
                style={"margin-left": "80px", "margin-top": "15px", "margin-bottom": "4px", 'float': 'left'}
            ), dcc.RadioItems(
                id='day-night-select',
                options=[{'label': i, 'value': i} for i in ['Day', 'Night', 'Complete']],
                value='Complete',
                labelStyle={'display': 'inline-block'},
                style={"margin-left": "20px", "margin-top": "19px", 'float': 'left'}
            )], style={"margin-left": "10px", "margin-bottom": "10px", "display": "table-row"}),
        html.Div(
            [html.Div(dcc.Graph(id='basic-map',figure=fig, style={'height': "75vh"}),
                      style={"width": "70%", "height": "99%", "border": "1px solid black", "float": "left"},
                      className="one-third column",
                      ),
             html.Div([html.Div(id='output-container-date-picker-range'),
                       html.Div(id='output-point-click'),
                       dash_table.DataTable(
                           id='table',
                           columns=[{"name": i, "id": i} for i in df.columns],
                           data=df.to_dict('records'),
                           style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                           style_cell={
                               'backgroundColor': 'rgb(50, 50, 50)',
                               'color': 'white'
                           },
                            style_table={
                                'maxHeight': '75vh',
                                'overflowY': 'scroll'
                            })
                       ], style={"width": "25%", "height": "99%", "border": "1px solid black", "float": "right"})],
            style={"width": "99%", "height": "80vh", "border": "1px solid black", "margin-left": "10px"}),

    ], style={"border": "1px solid black"})
