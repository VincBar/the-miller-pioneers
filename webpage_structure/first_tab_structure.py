import dash_core_components as dcc
import dash_html_components as html
import datetime as date

from urllib.request import urlopen
import json
import pandas as pd
import plotly.express as px
from datetime import date

with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                 dtype={"fips": str})

fig = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='unemp',
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=3, center={"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'unemp': 'unemployment rate'}
                           )
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
