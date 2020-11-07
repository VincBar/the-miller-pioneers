import dash_core_components as dcc
import dash_html_components as html
from datetime import date


def main_structure():
    return html.Div([
        html.Div([dcc.DatePickerRange(
            id='date-range-trouble',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date(2017, 9, 19),
            initial_visible_month=date(2017, 8, 5),
            start_date=date(2017, 7, 25),
            end_date=date(2017, 8, 25),
            style={"margin-left": "80px", "margin-top": "15px"}
        )], style={"margin-left": "10px", "margin-bottom": "10px"})
        ,
        html.Div([html.Div(style={"width": "31%", "height": "99%", "border": "1px solid black", "float": "left","margin-left":"10px"}),
                  html.Div(style={"width": "31%", "height": "99%", "border": "1px solid black", "float": "left","margin-left":"10px"}),
                  html.Div(style={"width": "31%", "height": "99%", "border": "1px solid black", "float": "left","margin-left":"10px"})],
                 style={"width": "99%", "height": "80vh", "border": "1px solid black"})
    ])
