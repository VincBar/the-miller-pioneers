
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div([
    dcc.Tabs(id='tabs-example', value='tab-1', children=[
        dcc.Tab(label='Switzerland Overview', value='tab-1'),
        dcc.Tab(label='Trouble Analysis', value='tab-2'),
    ]),
    html.Div(id='tabs-example-content')
],style={"height":"95vh","border":"1px solid black"}
)

#[html.H4("Map of switzerland",style={"float":"left"})]
#[html.H4("Interesting Information",style={"float":"right"})]
@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div([html.Div(style={"width":"70%","height":"99%","border":"1px solid black","float":"left"}),
                      html.Div(style={"width":"25%","height":"99%","border":"1px solid black","float":"right"})],
                     style={"width":"99%","height":"80vh","border":"1px solid black"})
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3('Tab content 2')
        ])

# need vh for now later will scale to the size of the content
if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)


import plotly.graph_objects as go

