import dash, json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from webpage_structure import first_tab_structure as first
from webpage_structure import second_tab_structure as second

from data_load.loader import BigLineLoader
from data_load.utils import line_info
import plotly.express as px
import plotly.graph_objects as go


import pandas as pd
import numpy as np
from datetime import date
from webpage_structure.first_tab_structure import troubleLoader

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# load map data
map_data = BigLineLoader().set_sort_km().load()
all_lines, abbr_dict = line_info(map_data)
map_layout = dict(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        mapbox_zoom=6,
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

# draw normal lines
drawn_lines = 0
for i, (k, line) in enumerate(all_lines.items()):
    line_dict = dict(mode="markers+lines",
                     lon=line['lon'],
                     lat=line['lat'],
                     marker={'size': 5, 'color': 'green'},
                     line={'color': "green"})
    if i == 0:
        fig = go.Figure(go.Scattermapbox(**line_dict))

    if line['n_stop'] > 8:
        drawn_lines += 1
        fig.add_trace(go.Scattermapbox(**line_dict))

fig.update_layout(**map_layout)




app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    dcc.Tabs(id='tabs-example', value='tab-2', children=[
        dcc.Tab(label='Switzerland Overview', value='tab-1'),
        dcc.Tab(label='Trouble Analysis', value='tab-2'),
    ]),
    html.Div(id='tabs-example-content')
], style={"height": "95vh", "border": "1px solid black"}
)


@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return first.main_structure()
    elif tab == 'tab-2':
        return second.main_structure()


@app.callback(
    Output('output-point-click', 'children'),
    [Input('basic-map', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


#
@app.callback(
    [dash.dependencies.Output('table', 'data'),
     dash.dependencies.Output('basic-map', 'figure'),],
    [dash.dependencies.Input('date-range-graphic', 'start_date'),
     dash.dependencies.Input('date-range-graphic', 'end_date'),
     dash.dependencies.Input('day-night-select', 'value')])
def update_output(start_date, end_date, value):
    troubleLoader.filter_by_time(start_date, end_date)
    if value == 'Day':
        filter = np.logical_not(np.in1d(troubleLoader.working_dataset.loc[:, 'umsetzung_intervalltyp_umleitung'],
                                        ["Sperre Bahnhof Nacht", "Sperre Strecke Nacht"]))
        df = troubleLoader.working_dataset.loc[
            filter, ["bp_to", "bp_from", "reduction_capacity", "date_to", "date_from"]]
    elif value == 'Night':
        filter = np.logical_not(np.in1d(troubleLoader.working_dataset.loc[:, 'umsetzung_intervalltyp_umleitung'],
                                        ["Sperre Bahnhof Tag", "Sperre Strecke Tag"]))
        df = troubleLoader.working_dataset.loc[
            filter, ["bp_to", "bp_from", "reduction_capacity", "date_to", "date_from"]]
    else:
        df = troubleLoader.working_dataset.loc[
             :, ["bp_to", "bp_from", "reduction_capacity", "date_to", "date_from"]]

    df.loc[:, "date_to"] = pd.DatetimeIndex(df.loc[:, "date_to"]).strftime("%Y-%m-%d")
    df.loc[:, "date_from"] = pd.DatetimeIndex(df.loc[:, "date_from"]).strftime("%Y-%m-%d")

    fig.data = fig.data[:drawn_lines]

    for index, issue in df.iterrows():
        try:
            line_dict = dict(mode="markers+lines",
                             lon=[abbr_dict[issue['bp_from']]['lon'], abbr_dict[issue['bp_to']]['lon']],
                             lat=[abbr_dict[issue['bp_from']]['lat'], abbr_dict[issue['bp_to']]['lat']],
                             marker={'size': 10, 'color': 'red'},
                             line={'color': 'red'})
            fig.add_trace(go.Scattermapbox(**line_dict))
        except:
            print('Unknown station')

    # find stops that appear in bp_to or bp_from
    # paint red

    return df.to_dict("records"), fig


@app.callback(
    [dash.dependencies.Output('first_column', 'children'),
     dash.dependencies.Output('second_column', 'children'),
     dash.dependencies.Output('third_column', 'children')],
    [dash.dependencies.Input('ordering-selection', 'value')]
)
def content_update(ordering_selection):
    print(ordering_selection)
    if ordering_selection == "severe":
        return second.severe(column=0), second.severe(column=1), second.severe(column=2)
    elif ordering_selection == "normal":
        return second.severe(column=0), second.severe(column=1), second.severe(column=2)
    elif ordering_selection == "capcity":
        return second.severe(column=0), second.severe(column=1), second.severe(column=2)
    elif ordering_selection == "time":
        return second.severe(column=0), second.severe(column=1), second.severe(column=2)
    elif ordering_selection == "conflict":
        return second.conflict(column=0), second.conflict(column=1), second.conflict(column=2)
    else:
        print("hi")

# need vh for now later will scale to the size of the content
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
