import dash, json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from webpage_structure import first_tab_structure as first
from webpage_structure import second_tab_structure as second

from data_load.loader import BigLineLoader
import plotly.express as px

import pandas as pd
import numpy as np
from datetime import date
from webpage_structure.first_tab_structure import troubleLoader

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
server = app.server

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
)

app.layout = html.Div([
    dcc.Tabs(id='tabs-example', value='tab-2', children=[
        dcc.Tab(label='Switzerland Overview', value='tab-1'),
        dcc.Tab(label='Trouble Analysis', value='tab-2'),
    ]),
    html.Div(id='tabs-example-content')
],
    id="mainContainer",
    style={"height": "95vh"},
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
     dash.dependencies.Output('basic-map', 'figure'), ],
    [dash.dependencies.Input('date-range-graphic', 'start_date'),
     dash.dependencies.Input('date-range-graphic', 'end_date'),
     dash.dependencies.Input('day-night-select', 'value')])
def update_output(start_date, end_date, value):
    troubleLoader.filter_by_time(start_date, end_date)
    if value == 'Day':
        filter = np.logical_not(np.in1d(troubleLoader.working_dataset.loc[:, 'umsetzung_intervalltyp_umleitung'],
                                        ["Sperre Bahnhof Nacht", "Sperre Strecke Nacht"]))
        df = troubleLoader.working_dataset.loc[
            filter, ["bp_to", "bp_from", "reduction_capacity","date_from","date_to"]]
    elif value == 'Night':
        filter = np.logical_not(np.in1d(troubleLoader.working_dataset.loc[:, 'umsetzung_intervalltyp_umleitung'],
                                        ["Sperre Bahnhof Tag", "Sperre Strecke Tag"]))
        df = troubleLoader.working_dataset.loc[
            filter, ["bp_to", "bp_from", "reduction_capacity", "date_from","date_to"]]
    else:
        df = troubleLoader.working_dataset.loc[
             :, ["bp_to", "bp_from", "reduction_capacity", "date_from","date_to"]]

    df.loc[:, "date_to"] = pd.DatetimeIndex(df.loc[:, "date_to"]).strftime("%Y-%m-%d")
    df.loc[:, "date_from"] = pd.DatetimeIndex(df.loc[:, "date_from"]).strftime("%Y-%m-%d")

    # TODO: do not create from scratch
    issues = df['bp_to'].to_list() + df['bp_from'].to_list()

    d = BigLineLoader().set_sort_km().load()
    d = d.rename(columns={'latitude': 'lat', 'longitude': 'lon'})
    d['line_group'] = d['linie']
    d['color'] = ['green'] * len(d)
    d.loc[d['abkurzung_bpk'].isin(issues), 'color'] = 'red'

    fig = px.line_mapbox(d, lat="lat", lon="lon", hover_name="bezeichnung_bps", hover_data=["linienname", "linie"],
                         line_group='line_group', color='color')
    fig.update_layout(
        mapbox_zoom=6,
        # hardcoded values for center of switzerland, can be adjusted automagically when we have the data
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
    # find stops that appear in bp_to or bp_from
    # paint red

    return df.to_dict("records"), fig


@app.callback(
    [dash.dependencies.Output('first_column', 'children'),
     dash.dependencies.Output('second_column', 'children'),
     dash.dependencies.Output('third_column', 'children')],
    [dash.dependencies.Input('ordering-selection', 'value'),
     dash.dependencies.Input('date-range-trouble', 'start_date'),
     dash.dependencies.Input('date-range-trouble', 'end_date'), ]
)
def content_update(ordering_selection, start_date, end_date):
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
        return second.conflict(0, start_date, end_date), second.conflict(1, start_date, end_date), second.conflict(2,
                                                                                                                   start_date,
                                                                                                                   end_date)
    else:
        print("hi")


# need vh for now later will scale to the size of the content
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
