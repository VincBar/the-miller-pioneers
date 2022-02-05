from dash import dcc
from dash import html

from datetime import date
from dash import dash_table
from data_load.loader import LineLoader, ConstructionSiteLoader
from data_load.trouble_management import TroubleManager

line_data = LineLoader().load()
construction_data = ConstructionSiteLoader().load()
troubleLoader = TroubleManager(construction_data, line_data)
troubleLoader.filter_by_time(date(2020, 7, 11), date(2025, 7, 11))
df = troubleLoader.working_dataset.loc[:, ["bp_to", "bp_from", "reduction_capacity", "date_from", "date_to"]]

troubleLoader.filter_by_time(date(2020, 7, 11), date(2025, 7, 11))
df = troubleLoader.working_dataset.loc[:, ["bp_to", "bp_from", "reduction_capacity", "date_from", "date_to"]]


def main_structure():
    names = ["From BP", "To BP", "Red. Capacity", "Building from", "Building till"]
    return html.Div([
        html.Div([
            dcc.DatePickerRange(
                id='date-range-graphic',
                min_date_allowed=date(2020, 7, 11),
                max_date_allowed=date(2050, 7, 11),
                initial_visible_month=date(2020, 7, 11),
                start_date=date(2020, 7, 11),
                end_date=date(2021, 7, 11),
                style={"margin-left": "80px", "margin-top": "15px", "margin-bottom": "15px", 'float': 'left',
                       "className": "dcc_control"}
            ), dcc.RadioItems(
                id='day-night-select',
                options=[{'label': i, 'value': i} for i in ['Day \t', 'Night \t', '24h \t']],
                value='Complete',
                labelStyle={'display': 'inline-block'},
                inputStyle={"margin-left": "20px", "margin-right": "10px"},
                style={"margin-left": "20px", "margin-top": "23px", 'float': 'left', "className": "dcc_control"}
            )], style={"margin-left": "10px", "margin-bottom": "10px", "display": "table-row"}),
        html.Div(
            [html.Div(dcc.Graph(id='basic-map', style={'height': "75vh"}),
                      style={"width": "67%",
                             "height": "80vx",
                             "border": "3px inset grey",
                             "float": "left",
                             "-webkit-box-shadow": "4px 4px 2px 0px rgba(50, 50, 50, 0.75)",
                             "-moz-box-shadow": "4px 4px 2px 0px rgba(50, 50, 50, 0.75)",
                             "box-shadow": "4px 4px 2px 0px rgba(50, 50, 50, 0.75)"},
                      className="one-third column",
                      ),
             html.Div([html.Div([html.H6('Disturbances in the selected period:')]),
                       html.Div(id='output-container-date-picker-range'),
                       html.Div(dash_table.DataTable(
                           id='table',
                           columns=[{"name": names[j], "id": i} for j, i in enumerate(df.columns)],
                           data=df.to_dict('records'),
                           style_header={'backgroundColor': 'rgb(30, 30, 30)'},
                           style_cell={
                               'textAlign': 'left',
                               'backgroundColor': 'rgb(50, 50, 50)',
                               'color': 'white'
                           },
                           style_table={
                               'maxHeight': '75vh',
                               'overflowY': 'scroll',
                               'margin-left': '6px',
                               'margin-right': '6px',
                               'margin-bottom': '6px'
                           })),
                       html.Div([html.P('Click on a disturbance to get more info.')]),
                       html.Div(id='output-point-click')

                       ],
                      style={"width": "24%",
                             "height": "70vx",
                             "border": "1px solid black",
                             "float": "left",
                             "margin-left": "20px",
                             "-webkit-box-shadow": "4px 4px 2px 0px rgba(50, 50, 50, 0.75)",
                             "-moz-box-shadow": "4px 4px 2px 0px rgba(50, 50, 50, 0.75)",
                             "box-shadow": "4px 4px 2px 0px rgba(50, 50, 50, 0.75)"})],
            style={"width": "99%",
                   "height": "80vh",
                   "margin-left": "10px",
                   }
        ),
    ])
# "-webkit-box-shadow": "7px 7px 5px 0px rgba(50, 50, 50, 0.75)",
#                    "-moz-box-shadow": "7px 7px 5px 0px rgba(50, 50, 50, 0.75)",
#                    "box-shadow": "7px 7px 5px 0px rgba(50, 50, 50, 0.75)"}
