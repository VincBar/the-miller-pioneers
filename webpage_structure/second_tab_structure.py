import dash_core_components as dcc
import dash_html_components as html
from datetime import date
import dash_table
import pandas as pd
from webpage_structure.first_tab_structure import troubleLoader
import plotly.express as px
import numpy as np
from data_load.loader import ConstructionSiteLoader, RoutesLoader
from data_load.trouble_management import TroubleManager
import plotly.graph_objects as go

d1 = ConstructionSiteLoader().load()
routes = RoutesLoader().load()

t = TroubleManager(d1, routes)


def main_structure():
    return html.Div([
        html.Div([
            dcc.DatePickerRange(
                id='date-range-trouble',
                min_date_allowed=date(2020, 7, 11),
                max_date_allowed=date(2050, 7, 11),
                initial_visible_month=date(2020, 7, 11),
                start_date=date(2020, 7, 11),
                end_date=date(2022, 7, 11),
                style={"margin-left": "80px", "margin-top": "15px", "margin-bottom": "4px", 'float': 'left'}
            ),
            dcc.RadioItems(
                id='ordering-selection',
                options=[{'label': 'Most severe', 'value': 'severe'},
                         # {'label': 'Highest normal traffic', 'value': 'normal'},
                         # {'label': 'Highest Capacity Reduction', 'value': "capacity"},
                         # {'label': 'Most Days with Reduction', 'value': 'time'},
                         {'label': 'Most Conflicts', 'value': 'conflict'}, ],
                value='conflict',
                labelStyle={'display': 'inline-block'},
                style={"margin-left": "20px", "margin-top": "23px", 'float': 'left'})
        ],
            style={"margin-left": "10px", "margin-bottom": "10px", "display": "table-row", "width": "100%"})
        ,
        html.Div([html.Div(id="first_column",
                           style={"width": "31%", "height": "99%", "float": "left",
                                  "margin-left": "10px",
                                  "border": "3px inset grey",
                                  "-webkit-box-shadow": "4px 4px 2px 0px rgba(50, 50, 50, 0.75)",
                                  "-moz-box-shadow": "4px 4px 2px 0px rgba(50, 50, 50, 0.75)",
                                  "box-shadow": "4px 4px 2px 0px rgba(50, 50, 50, 0.75)"}),
                  html.Div(id="second_column",
                           style={"width": "31%", "height": "99%", "float": "left",
                                  "margin-left": "10px",
                                  "border": "3px inset grey",
                                  "-webkit-box-shadow": "4px 4px 2px 0px rgba(50, 50, 50, 0.75)",
                                  "-moz-box-shadow": "4px 4px 2px 0px rgba(50, 50, 50, 0.75)",
                                  "box-shadow": "4px 4px 2px 0px rgba(50, 50, 50, 0.75)"}),
                  html.Div(id="third_column",
                           style={"width": "31%", "height": "99%", "float": "left",
                                  "margin-left": "10px",
                                  "border": "3px inset grey",
                                  "-webkit-box-shadow": "4px 4px 2px 0px rgba(50, 50, 50, 0.75)",
                                  "-moz-box-shadow": "4px 4px 2px 0px rgba(50, 50, 50, 0.75)",
                                  "box-shadow": "4px 4px 2px 0px rgba(50, 50, 50, 0.75)"})],
                 style={"width": "99%", "height": "80vh"})
    ])


def most_severe(start_time, end_time):
    t.filter_by_time(start_time, end_time)
    constr = t.working_dataset

    # find where bp_from in constr set matches routes bp_from
    routes_constr = pd.merge(routes, constr, on="bp_from")
    routes_constr = routes_constr.rename(columns={"bp_to_x": "bp_to_line", "bp_to_y": "bp_to_constr"})
    routes_constr["cancelled_trains"] = routes_constr["num_trains"] * routes_constr["reduction_capacity"]

    routes_constr["cancelled_trains"] = routes_constr["cancelled_trains"] * (
            routes_constr["date_to"] - routes_constr["date_from"]).apply(lambda x: x.days) / 365
    routes_constr["trains_complete_time"] = routes_constr["num_trains"] * (
            routes_constr["date_to"] - routes_constr["date_from"]).apply(lambda x: x.days) / 365
    routes_constr.sort_values("cancelled_trains", ascending=False, inplace=True)
    five_most_critical = routes_constr.iloc[0:10, :]

    return five_most_critical


from datetime import date


def severe(column=0, start_date=date(2020, 7, 11), end_date=date(2021, 7, 11)):
    # some getting df stuff.

    tmp = most_severe(start_date, end_date)

    tmp = tmp.loc[:, ["umsetzung_intervalltyp_umleitung", "reduction_capacity", "num_trains", "cancelled_trains"]]
    names = ["Index", "Construction", "Red. Capacity", "Usual Trains", "Red. Train Capacity"]
    tmp.reset_index(inplace=True)
    tmp = tmp.round(2)
    return html.Div([
        html.H6("Strongest Reduction on Train Numbers"),
        dash_table.DataTable(
            id='table_focus_{}'.format(column),
            columns=[{"name": names[j], "id": i} for j, i in enumerate(tmp.columns)],
            data=tmp.to_dict('records'),
            style_table={
                'overflowY': 'scroll'
            }
        )
    ], style={"margin-top": "20px"})


def severe_plot(column=1, start_date=date(2020, 7, 11), end_date=date(2021, 7, 11)):
    # some getting df stuff.
    tmp = most_severe(start_date, end_date)
    tmp.reset_index(inplace=True)
    if column == 1:
        tmp = tmp[:5]
    else:
        tmp = tmp[5:10]
    animals = ["Construction {}".format(el) for el in tmp["index"]]

    fig = go.Figure(data=[
        go.Bar(name='Original accumulated capacity', x=animals, y=tmp["trains_complete_time"],),
        go.Bar(name='Left accumulated capacity', x=animals, y=tmp["trains_complete_time"] - tmp["cancelled_trains"])
    ])
    # Change the bar mode
    fig.update_layout(barmode='group')
    if column == 1:
        return html.Div([
            html.H6("Reduction on Train Numbers Visualized top 1-5"),
            dcc.Graph(id='reduction-bar-low-{}'.format(column), figure=fig, style={'height': "50vh", "width": "100%"})]
            , style={"margin-top": "20px"})
    else:
        return html.Div([
            html.H6("Reduction on Train Numbers top 6-10"),
            dcc.Graph(id='reduction-bar-low-{}'.format(column), figure=fig, style={'height': "50vh", "width": "100%"})]
            , style={"margin-top": "20px"})


def severe_empty(column=1, start_date=date(2020, 7, 11), end_date=date(2021, 7, 11)):
    return html.Div()


def reformat_datetime(df, columns_relevant):
    df.loc[:, "date_to"] = pd.DatetimeIndex(df.loc[:, "date_to"]).strftime("%Y-%m-%d")
    df.loc[:, "date_from"] = pd.DatetimeIndex(df.loc[:, "date_from"]).strftime("%Y-%m-%d")

    return df.loc[:, columns_relevant]


def conflict(column=0, start_time=date(2020, 7, 11), end_time=date(2025, 7, 11)):
    if len(troubleLoader.get_conflicts_in_timeframe(start_time, end_time)) <= column:
        return html.Div([html.H6("No more unscheduled conflicts", style={"text-align": "centre"})])
    else:
        df_in = pd.DataFrame(
            troubleLoader.get_conflicts_in_timeframe(start_time, end_time)[-(column + 1)][0]).transpose()
        df_in.reset_index(inplace=True)
        df_conflict = pd.DataFrame(
            troubleLoader.get_conflicts_in_timeframe(start_time, end_time)[-(column + 1)][1])
        df_conflict.reset_index(inplace=True)
        df_in = reformat_datetime(df_in, ["index", "reduction_capacity", "date_from", "date_to"])
        df_conflict = reformat_datetime(df_conflict,
                                        ["index", "umsetzung_intervalltyp_umleitung", "reduction_capacity", "date_from",
                                         "date_to"])
        df = pd.concat([df_in, df_conflict])
        df.loc[:, "index"] = ["Job {}".format(el) for el in df["index"].values]
        names_1 = ["Identifier", "Red. Capacity", "Building from", "Building till"]

        names_2 = ["Identifier", "Umsetzung", "Red. Capacity", "Building from", "Building till"]

        time_plot = px.timeline(df, x_start="date_from", x_end="date_to", y="index", color="reduction_capacity",
                                color_continuous_scale=px.colors.sequential.YlOrRd)
        time_plot.update_yaxes(autorange="reversed")
        time_plot.update_layout(xaxis=dict(tickformat="%Y-%m"))
        time_plot.update_layout(yaxis={"title": ""})
        # otherwise tasks are listed from the bottom up
        return html.Div([
            html.Div([
                html.H6("Planned Project", style={"text-align": "centre"}),
                dash_table.DataTable(
                    id='table_in_{}'.format(column),
                    columns=[{"name": names_1[j], "id": i} for j, i in enumerate(df_in.columns)],
                    data=df_in.to_dict('records'),
                    style_table={
                        'overflowX': 'scroll'
                    }
                ),
                html.H6("Conflicting Projects", style={"text-align": "centre"}),
                dash_table.DataTable(
                    id='table_focus_{}'.format(column),
                    columns=[{"name": names_2[j], "id": i} for j, i in enumerate(df_conflict.columns)],
                    data=df_conflict.to_dict('records'),
                    style_table={
                        'overflowX': 'scroll'
                    })], style={"height": "30vh"}),
            dcc.Graph(id='basic-time-{}'.format(column), figure=time_plot, style={'height': "45vh", "width": "100%"})
        ])
