import dash_core_components as dcc
import dash_html_components as html
from app import app
from dash.dependencies import Input,Output,State
from fbprophet.plot import plot_plotly
import pandas as pd
from model import generateModel
from utility import parseContents


forecastTab = dcc.Loading(
    html.Div(
        id = 'forecastTab'
    )
)    


@app.callback(
    Output('forecastTab', 'children'),
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
def createPlot(signal, frequency, holidayDropdown, holidayScale, seasonalityScale, changepointScale, seasonalityMode, contents, filename, paramSearch):
    print(signal, frequency, holidayDropdown, holidayScale, seasonalityScale, changepointScale, seasonalityMode, filename, paramSearch)
    if signal == 'VOID':
        return None
    elif signal == 'FAILURE':
        return html.Div('Encountered an error : ' + str(e))

    df = parseContents(contents, filename)
    model = generateModel(frequency, holidayDropdown, holidayScale, seasonalityScale, changepointScale, seasonalityMode, df, paramSearch)
    future = model.make_future_dataframe(periods = int(0.1 * len(df)), freq = frequency)
    forecast = model.predict(future)
    fig = plot_plotly(model, forecast, xlabel = 'Date', ylabel = 'Value')
    return dcc.Graph(figure = fig)


