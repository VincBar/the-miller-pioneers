import dash_core_components as dcc
import dash_html_components as html
from datetime import date
import dash_table
import pandas as pd
from webpage_structure.first_tab_structure import troubleLoader

def main_structure():
    return html.Div([
        html.Div([
            dcc.DatePickerRange(
                id='date-range-trouble',
                min_date_allowed=date(2020, 7, 11),
                max_date_allowed=date(2050, 7, 11),
                initial_visible_month=date(2020, 7, 11),
                start_date=date(2020, 7, 11),
                end_date=date(2021, 7, 11),
                style={"margin-left": "80px", "margin-top": "15px", "margin-bottom": "4px", 'float': 'left'}
            ),
            html.Div(dcc.Dropdown(
                id='ordering-selection',
                options=[
                    {'label': 'Most severe', 'value': 'severe'},
                    {'label': 'Highest normal traffic', 'value': 'normal'},
                    {'label': 'Highest Capacity Reduction', 'value': "capacity"},
                    {'label': 'Most Days with Reduction', 'value': 'time'},
                    {'label': 'Most Conflicts', 'value': 'conflict'},
                ],
                value='severe',
                style={"margin-left": "20px", "margin-top": "19px","width":"400px"}
            ),style={'float': 'right'})], style={"margin-left": "10px", "margin-bottom": "10px", "display": "table-row","width":"100%"})
        ,
        html.Div([html.Div(id="first_column",
                           style={"width": "31%", "height": "99%", "border": "1px solid black", "float": "left",
                                  "margin-left": "10px"}),
                  html.Div(id="second_column",
                           style={"width": "31%", "height": "99%", "border": "1px solid black", "float": "left",
                                  "margin-left": "10px"}),
                  html.Div(id="third_column",
                           style={"width": "31%", "height": "99%", "border": "1px solid black", "float": "left",
                                  "margin-left": "10px"})],
                 style={"width": "99%", "height": "80vh", "border": "1px solid black"})
    ])

import numpy as np


def severe(column=0):
    # some getting df stuff.
    df = pd.DataFrame(np.ones((6,2)), index=["Usual Number of Trains",
                                       "Usual Freight Capacity",
                                       "Reduced Train Capacity",
                                       "Reduced Freight Capacity",
                                       "Difference in Trains",
                                       "Difference in Freight"])
    df.reset_index(inplace=True)

    return html.Div([
        dash_table.DataTable(
            id='table_focus_{}'.format(column),
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'))
    ])

def conflict(column=0,starttime=date(2020, 7, 11),endtime=date(2025,7,11)):
    df_in = pd.DataFrame(troubleLoader.get_conflicts_in_timeframe(date(2020, 7, 11),date(2025,7,11))[column][0])
    df_conflict = pd.DataFrame(troubleLoader.get_conflicts_in_timeframe(date(2020, 7, 11),date(2025,7,11))[column][1]).transpose()

    return html.Div([
        dash_table.DataTable(
            id='table_in_{}'.format(column),
            columns=[{"name": i, "id": i} for i in df_in.columns],
            data=df_in.to_dict('records')),
        dash_table.DataTable(
            id='table_focus_{}'.format(column),
            columns=[{"name": i, "id": i} for i in df_conflict.columns],
            data=df_conflict.to_dict('records'))
    ])

