from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from fbprophet.plot import plot_cross_validation_metric
from model import generateModel
from fbprophet.diagnostics import cross_validation, performance_metrics
from utility import parseContents
from plotly.tools import mpl_to_plotly

diagnosticsTab = dcc.Loading(
    html.Div(
        id = 'diagnosticsTab'
    )
)    


@app.callback(
    Output('diagnosticsTab', 'children'),
    [Input('signal', 'children')],
    [State('frequency', 'value'),
     State('holidayDropdown', 'value'),
     State('holidayScale', 'value'),
     State('seasonalityScale', 'value'),
     State('changepointScale', 'value'),
     State('seasonalityMode', 'value'),
     State('file', 'contents'),
     State('file', 'filename'),
     State('paramSearch', 'value')]
)
def createDiagnosticsLayout(signal, frequency, holidayDropdown, holidayScale, seasonalityScale, changepointScale, seasonalityMode, contents, filename, paramSearch):
    print(signal, frequency, holidayDropdown, holidayScale, seasonalityScale, changepointScale, seasonalityMode, filename, paramSearch)
    if signal == 'VOID':
        return None
    elif signal == 'FAILURE':
        return html.Div('Encountered an error : ' + str(e))
    df = parseContents(contents, filename)
    model = generateModel(frequency, holidayDropdown, holidayScale, seasonalityScale, changepointScale, seasonalityMode, df, paramSearch)
    initial, period, horizon =  getParams(frequency, len(df))
    df_cv =cross_validation(model, initial = initial, period = period, horizon = horizon)
    #df_p = performance_metrics(df_cv, rolling_window = 0)
    #print(df_p.head())
    fig = mpl_to_plotly(plot_cross_validation_metric(df_cv, metric = 'mae', rolling_window = 0))
    return html.Div(children = [html.H6('Mean Absolute Error', style = {'margin-left': '1rem'}), dcc.Graph(figure = fig)])
    
def getParams(freq, n):
    if freq == 'D':
        return str(int(0.5*n)) + ' days', str(int(0.1*n)) + ' days', str(int(0.1*n)) + ' days'
    elif freq == 'W':
        return str(int(0.5*7*n)) + ' days', str(int(0.1*7*n)) + ' days', str(int(0.1*7*n)) + ' days'
    elif freq == 'M':
        return str(int(0.5*30.5*n)) + ' days', str(int(0.1*30.5*n)) + ' days', str(int(0.1*30.5*n)) + ' days'
    elif freq == 'A':
        return str(int(0.5*365*n)) + ' days', str(int(0.1*365*n)) + ' days', str(int(0.1*365*n)) + ' days'
    elif freq == 'Q':
        return str(int(0.5*91.3*n)) + ' days', str(int(0.1*91.3*n)) + ' days', str(int(0.1*91.3*n)) + ' days'
    elif freq == 'H':
        return str(int(0.5*n)) + ' hours', str(int(0.1*n)) + ' hours', str(int(0.1*n)) + ' hours'

