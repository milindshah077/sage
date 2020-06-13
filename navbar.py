import dash_bootstrap_components as dbc
import dash_html_components as html
from forecastTab import forecastTab
from trendTab import trendTab
from diagnosticsTab import diagnosticsTab

NAVBAR_STYLE = {
    #'position' : 'sticky',
    #'top' : 0,
    #'right' : 0,
    'margin-left': '16rem',
    'height' : '5rem',
    'background-color' : '#1E90FF'
}
tabs = html.Div(
    dbc.Tabs(
        [
            dbc.Tab(forecastTab, label='Interactive Forecast Plot', tab_style = {'height' : '5rem'}, label_style = {'line-height' : '4rem'}, style = {'width' : '100%', 'margin' : '2rem auto'}),
            dbc.Tab(trendTab, label='Trend Breakdown', tab_style = {'height' : '5rem'}, label_style ={'line-height' : '4rem'}, style = {'width' : '100%', 'margin' : '2rem auto'}),
            dbc.Tab(diagnosticsTab, label='Model Diagnostics', tab_style = {'height' : '5rem'}, label_style = {'line-height' : '4rem'}, style = {'width' : '100%', 'margin' : '2rem auto'}),
        ]
    ),
    style = NAVBAR_STYLE
)
        

    
