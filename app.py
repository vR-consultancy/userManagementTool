import dash,os
from layout import mainLayout
from callbacks import register_callbacks
import dash_bootstrap_components as dbc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_scripts = ['https://cdn.plot.ly/plotly-locale-nl-latest.js']
# app = dash.Dash(__name__)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE ],external_scripts=external_scripts)

app.layout = mainLayout
#--! Set Dash to suppress callback exceptions, because some callbacks can only be made when the first callback in the main layout has been made.
app.config['suppress_callback_exceptions'] = False
register_callbacks(app)

safe = True 
if safe:
    host = '127.0.0.1'
else:
    host = '0.0.0.0'

if __name__ == '__main__':
    app.run_server(debug=True,host=host, port=8051)