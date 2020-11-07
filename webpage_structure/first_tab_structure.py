import dash_core_components as dcc
import dash_html_components as html
import datetime as date

from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px
from datetime import date

# dummy data for plotting
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")
fig = px.scatter_mapbox(us_cities, lat="lat", lon="lon", hover_name="City", hover_data=["State", "Population"],
                        color_discrete_sequence=["fuchsia"])
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


def main_structure():
    return html.Div([
        html.Div([html.Div(dcc.Graph(figure=fig),
                           style={"width": "70%", "height": "99%", "border": "1px solid black", "float": "left"},
                           className="one-third column",
                           ),
                  html.Div(id='output-container-date-picker-range',
                           style={"width": "25%", "height": "99%", "border": "1px solid black", "float": "right"})],
                 style={"width": "99%", "height": "80vh", "border": "1px solid black"}),
        html.Div([dcc.DatePickerRange(
            id='date-range-graphic',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date(2017, 9, 19),
            initial_visible_month=date(2017, 8, 5),
            end_date=date(2017, 8, 25)
        )],
        ),
    ])
