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
import dash_table
import pandas as pd
import numpy as np
from datetime import date
from webpage_structure.first_tab_structure import troubleLoader
from data_load.line_operating_points import filter_small_lines

external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']

# load map data
map_data = BigLineLoader().set_sort_km().load()
map_data = filter_small_lines(map_data)
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
                'https://tile.osm.ch/switzerland/{z}/{x}/{y}.png'
                # "http://a.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png"
            ]
        }
    ],
    showlegend=False)
# draw normal lines
drawn_lines = 0
for i, (k, line) in enumerate(all_lines.items()):
    line_dict = dict(mode="markers+lines",
                     name=str(line['line_number']),
                     # legendgroup='Lines',
                     opacity=0.5,
                     lon=line['lon'],
                     lat=line['lat'],
                     text=line['stop_name'],
                     # hoverinfo=line['stop_name'],
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
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
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
    [Input('basic-map', 'clickData'),
     dash.dependencies.Input('date-range-graphic', 'start_date'),
     dash.dependencies.Input('date-range-graphic', 'end_date'),
     ])
def display_click_data(clickData, start_date,end_date):
    troubleLoader.filter_by_time(start_date, end_date)
    df_1 = troubleLoader.working_dataset

    df_1.loc[:, "date_to"] = pd.DatetimeIndex(df_1.loc[:, "date_to"]).strftime("%Y-%m-%d")
    df_1.loc[:, "date_from"] = pd.DatetimeIndex(df_1.loc[:, "date_from"]).strftime("%Y-%m-%d")

    if clickData is None:
        return json.dumps(clickData, indent=2)
    else:
        index_list = np.logical_or(df_1.loc[:, "bp_from"] == clickData["points"][0]["text"],
                                   df_1.loc[:, "bp_to"] == clickData["points"][0]["text"])
        df_new=df_1.loc[index_list, :].transpose()
        df_new.reset_index(inplace=True)
        return dash_table.DataTable(
            id='table_new',
            columns=[{"name": i, "id": i} for j, i in enumerate(df_new.columns)],
            data=df_new.to_dict('records'),
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
                'textAlign': 'left',
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
            style_table={
                'maxHeight': '75vh',
                'overflowY': 'scroll'
            })


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
            filter, ["bp_to", "bp_from", "reduction_capacity", "date_from", "date_to"]]
    elif value == 'Night':
        filter = np.logical_not(np.in1d(troubleLoader.working_dataset.loc[:, 'umsetzung_intervalltyp_umleitung'],
                                        ["Sperre Bahnhof Tag", "Sperre Strecke Tag"]))
        df = troubleLoader.working_dataset.loc[
            filter, ["bp_to", "bp_from", "reduction_capacity", "date_from", "date_to"]]
    else:
        df = troubleLoader.working_dataset.loc[
             :, ["bp_to", "bp_from", "reduction_capacity", "date_from", "date_to"]]

    df.loc[:, "date_to"] = pd.DatetimeIndex(df.loc[:, "date_to"]).strftime("%Y-%m-%d")
    df.loc[:, "date_from"] = pd.DatetimeIndex(df.loc[:, "date_from"]).strftime("%Y-%m-%d")

    fig.data = fig.data[:drawn_lines]

    for index, issue in df.iterrows():
        if issue['reduction_capacity'] >= 0.5:
            color = 'red'
        else:
            color = 'yellow'

        try:
            line_dict = dict(mode="markers+lines",
                             name=issue['bp_from'] + '-' + issue['bp_to'],
                             # legendgroup='Construction',
                             text=[issue['bp_from'], issue['bp_to']],
                             # hoverinfo=[issue['date_from'] + '-' + issue['date_to']],
                             lon=[abbr_dict[issue['bp_from']]['lon'], abbr_dict[issue['bp_to']]['lon']],
                             lat=[abbr_dict[issue['bp_from']]['lat'], abbr_dict[issue['bp_to']]['lat']],
                             marker={'size': 10, 'color': color},
                             line={'color': color})
            fig.add_trace(go.Scattermapbox(**line_dict))
        except:
            print('unsuccessful: could not find abbreviation')

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
        return second.severe(column=0,start_date=start_date,end_date=end_date), second.severe_plot(column=1,start_date=start_date,end_date=end_date), second.severe_empty(column=2)
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
