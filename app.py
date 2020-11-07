import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from webpage_structure import first_tab_structure as first
from webpage_structure import second_tab_structure as second
from datetime import date
# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
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
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Input('date-range-graphic', 'start_date'),
     dash.dependencies.Input('date-range-graphic', 'end_date')])
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix

@app.callback(dash.dependencies.Output('output-day-night', 'children'),
              dash.dependencies.Input('day-night-select', 'value'))
def select_time_of_day(value):
    if value == 'Day':
        return "You want them day"
    elif value == 'Night':
        return "You want them night"
    else:
        return "You want it all"

# need vh for now later will scale to the size of the content
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
