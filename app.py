
import dash

import dash_html_components as html


app = dash.Dash(__name__)
server = app.server


app.layout = html.Div(
    [html.H1(children='I LIKE TRAINS')]
)

if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)