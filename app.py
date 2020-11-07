import dash, json
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from webpage_structure import first_tab_structure as first
from webpage_structure import second_tab_structure as second
import pandas as pd
import numpy as np
from datetime import date
from webpage_structure.first_tab_structure import troubleLoader

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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
    dash.dependencies.Output('table', 'data'),
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
    return df.to_dict("records")


@app.callback(
    [dash.dependencies.Output('first_column', 'children'),
    dash.dependencies.Output('second_column', 'children'),
    dash.dependencies.Output('third_column', 'children')],
    [dash.dependencies.Input('ordering-selection', 'value')]
)
def content_update(ordering_selection):
    if ordering_selection == "severe":
        return second.severe(column=0), second.severe(column=1), second.severe(column=2)
    if ordering_selection == "normal":
        return second.severe(column=0), second.severe(column=1), second.severe(column=2)
    if ordering_selection == "capcity":
        return second.severe(column=0), second.severe(column=1), second.severe(column=2)
    if ordering_selection == "time":
        return second.severe(column=0), second.severe(column=1), second.severe(column=2)
    if ordering_selection == "conflict":
        return second.severe(column=0), second.severe(column=1), second.severe(column=2)


# need vh for now later will scale to the size of the content
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
