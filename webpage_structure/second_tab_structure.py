import dash_core_components as dcc
import dash_html_components as html
import datetime as date


def main_structure():
    return html.Div([
        html.H4("Address the most pressing troubles"),
        html.Div([html.Div(style={"width": "31%", "height": "99%", "border": "1px solid black", "float": "left"}),
                  html.Div(style={"width": "31%", "height": "99%", "border": "1px solid black", "float": "left"}),
                  html.Div(style={"width": "31%", "height": "99%", "border": "1px solid black", "float": "left"})],
                 style={"width": "99%", "height": "80vh", "border": "1px solid black"})
    ])
