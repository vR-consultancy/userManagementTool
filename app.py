import dash,os
from layout import mainLayout
from callbacks import register_callbacks
import dash_bootstrap_components as dbc
import keyring, dash_auth

username = 'bedrijfsbureau'
password = keyring.get_password('dashScript', username)
VALID_USERNAME_PASSWORD_PAIRS = {username: password}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_scripts = ['https://cdn.plot.ly/plotly-locale-nl-latest.js']
# app = dash.Dash(__name__)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE ],external_scripts=external_scripts)


auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.config.suppress_callback_exceptions = True

app.layout = mainLayout
#--! Set Dash to suppress callback exceptions, because some callbacks can only be made when the first callback in the main layout has been made.

register_callbacks(app)

safe = False 
if safe:
    host = '127.0.0.1'
else:
    host = '0.0.0.0'

if __name__ == '__main__':
    app.run_server(debug=False,host=host, port=8051)