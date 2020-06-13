from app import app
import dash_html_components as html
from sidebar import sidebar
from logo import logo
from navbar import tabs

app.layout = html.Div([logo, sidebar, tabs, html.Div(id = 'signal', style = {'display' : 'none'})])

app.title = 'Sage'
if __name__ == '__main__':
    app.run_server(debug = True, host ='0.0.0.0', port = 8079)
