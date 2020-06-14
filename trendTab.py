from app import app
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from fbprophet.plot import plot_components_plotly, plot_seasonality_plotly, plot_components
from model import generateModel
from utility import parseContents
from plotly.tools import mpl_to_plotly

trendTab = dcc.Loading(
    html.Div(
        id = 'trendTab'
    )
)    


@app.callback(
    Output('trendTab', 'children'),
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
def createComponentLayout(signal, frequency, holidayDropdown, holidayScale, seasonalityScale, changepointScale, seasonalityMode, contents, filename, paramSearch):
    print(signal, frequency, holidayDropdown, holidayScale, seasonalityScale, changepointScale, seasonalityMode, filename, paramSearch)
    if signal == 'VOID':
        return None
    if signal != 'NOTIFY':
        return html.Div('Encountered an error : ' + signal, style = {'margin-left' : '1rem'})
    df = parseContents(contents, filename)
    model = generateModel(frequency, None, holidayScale, seasonalityScale, changepointScale, seasonalityMode, df, paramSearch)
    future = model.make_future_dataframe(periods = int(0.1*len(df)), freq = frequency)
    forecast = model.predict(future)
    fig = plot_components_plotly(model, forecast)
    return dcc.Graph(figure = fig)
