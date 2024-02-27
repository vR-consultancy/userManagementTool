import dash,os
from database import *
from functions import *
# version check
try:

    v = latestVersion()
    version = v[0]

    if version < 1.0:
        print('Outdated versie. Update draaien.')
        from update import update10
        update10()        
        
    else:
        pass


    v = latestVersion()
    version = v[0]

    if version < 1.1:
        print('Outdated versie. Update draaien.')
        from update import update11
        update11()       
    else:
        pass  

    v = latestVersion()
    version = v[0]

    if version < 1.2:
        print('Outdated versie. Update draaien.')
        from update import update12
        update12()       
    else:
        pass            

except:
    print('Kon versie niet checken! Aborted..')
    exit()


from layout import mainLayout
from callbacks import register_callbacks
import dash_bootstrap_components as dbc


import sys


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_scripts = ['https://cdn.plot.ly/plotly-locale-nl-latest.js']
# app = dash.Dash(__name__)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE ],external_scripts=external_scripts)




app.config.suppress_callback_exceptions = True

app.layout = mainLayout
#--! Set Dash to suppress callback exceptions, because some callbacks can only be made when the first callback in the main layout has been made.

register_callbacks(app)




try:
    if sys.argv[1].lower() in ['test','debug']:
        debug = True
    else:

        import keyring, dash_auth
        username = 'bedrijfsbureau'
        password = keyring.get_password('dashScript', username)
        VALID_USERNAME_PASSWORD_PAIRS = {username: password}

        debug = False 
        auth = dash_auth.BasicAuth(
            app,
            VALID_USERNAME_PASSWORD_PAIRS)
except:
    import keyring, dash_auth

    username = 'bedrijfsbureau'
    password = keyring.get_password('dashScript', username)
    VALID_USERNAME_PASSWORD_PAIRS = {username: password}
    debug = False 
    auth = dash_auth.BasicAuth(
        app,
        VALID_USERNAME_PASSWORD_PAIRS)

context = ('domain.crt','domain.key')
if debug:
    if __name__ == '__main__':
        app.run_server(debug=True,host='localhost', port=8050)
else:
    if __name__ == '__main__':
        app.run_server(debug=False,host='0.0.0.0', port=444, ssl_context=context)