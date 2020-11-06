
import dash

import dash_html_components as html


app = dash.Dash(__name__)
server = app.server


app.layout = html.Div(

)

if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)