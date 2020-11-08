import dash_core_components as dcc
import dash_html_components as html
from datetime import date
import dash_table
import pandas as pd
from webpage_structure.first_tab_structure import troubleLoader
import plotly.express as px
import numpy as np


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
            dcc.RadioItems(
                id='ordering-selection',
                options=[{'label': 'Most severe', 'value': 'severe'},
                         {'label': 'Highest normal traffic', 'value': 'normal'},
                         {'label': 'Highest Capacity Reduction', 'value': "capacity"},
                         {'label': 'Most Days with Reduction', 'value': 'time'},
                         {'label': 'Most Conflicts', 'value': 'conflict'}, ],
                value='conflict',
                labelStyle={'display': 'inline-block'},
                style={"margin-left": "20px", "margin-top": "19px", 'float': 'left'})
        ],
            style={"margin-left": "10px", "margin-bottom": "10px", "display": "table-row", "width": "100%"})
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




def severe(column=0):
    # some getting df stuff.
    df = pd.DataFrame(np.ones((6, 2)), index=["Usual Number of Trains",
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


def reformat_datetime(df, columns_relevant):
    df.loc[:, "date_to"] = pd.DatetimeIndex(df.loc[:, "date_to"]).strftime("%Y-%m-%d")
    df.loc[:, "date_from"] = pd.DatetimeIndex(df.loc[:, "date_from"]).strftime("%Y-%m-%d")

    return df.loc[:, columns_relevant]


def conflict(column=0, start_time=date(2020, 7, 11), end_time=date(2025, 7, 11)):
    if len(troubleLoader.get_conflicts_in_timeframe(start_time, end_time))<=column:
        return html.Div([html.H6("No more unscheduled conflicts")])
    else:
        df_in = pd.DataFrame(
            troubleLoader.get_conflicts_in_timeframe(start_time, end_time)[-(column + 1)][0]).transpose()
        df_in.reset_index(inplace=True)
        df_conflict = pd.DataFrame(
            troubleLoader.get_conflicts_in_timeframe(start_time, end_time)[-(column + 1)][1])
        df_conflict.reset_index(inplace=True)
        df_in = reformat_datetime(df_in, ["index","reduction_capacity", "date_from", "date_to"])
        df_conflict = reformat_datetime(df_conflict, ["index","umsetzung_intervalltyp_umleitung", "reduction_capacity", "date_from", "date_to"])
        df = pd.concat([df_in,df_conflict])
        df.loc[:,"index"]=["Job {}".format(el) for el in df["index"].values]
        names_1 = ["Identifier","Red. Capacity","Building from", "Building till"]

        names_2 = ["Identifier","Umsetzung", "Red. Capacity","Building from", "Building till"]

        time_plot = px.timeline(df, x_start="date_from", x_end="date_to", y="index",color="reduction_capacity")
        time_plot.update_yaxes(autorange="reversed")
        time_plot.update_xaxes(autorange="reversed")
        time_plot.update_layout(xaxis=dict(tickformat="%Y-%m"))
        # otherwise tasks are listed from the bottom up
        return html.Div([
            html.H6("Implementation not planned yet"),
            dash_table.DataTable(
                id='table_in_{}'.format(column),
                columns=[{"name": names_1[j], "id": i} for j,i in enumerate(df_in.columns)],
                data=df_in.to_dict('records'),
                style_table={
                    'overflowY': 'scroll'
                }
            ),
            html.H6("Conflicts to keep in mind"),
            dash_table.DataTable(
                id='table_focus_{}'.format(column),
                columns=[{"name": names_2[j], "id": i}  for j,i in enumerate(df_conflict.columns)],
                data=df_conflict.to_dict('records'),
                style_table={
                    'overflowY': 'scroll'
                }),
            dcc.Graph(id='basic-time-{}'.format(column), figure=time_plot, style={'height': "30vh","width":"100%"})
        ])

