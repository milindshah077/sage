import dash
import dash_bootstrap_components as dbc

external_stylesheet = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
dbc_stylesheet = dbc.themes.BOOTSTRAP
#FONT_AWESOME = "https://use.fontawesome.com/releases/v5.7.2/css/all.css"

app = dash.Dash(__name__, external_stylesheets = [dbc_stylesheet])
app.config.suppress_callback_exceptions = True
