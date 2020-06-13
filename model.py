from app import app
from dash.dependencies import Input,Output,State
from fbprophet import Prophet
import pandas as pd
from flask_caching import Cache
from utility import parseContents

CACHE_CONFIG = {
    'CACHE_TYPE' : 'filesystem',
    'CACHE_DIR': 'cache/',
    'CACHE_DEFAULT_TIMEOUT' : 300
}
cache = Cache()
cache.init_app(app.server, config = CACHE_CONFIG)


@app.callback(
    Output('signal', 'children'),
    [Input('submit', 'n_clicks')],
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
def signalModelGenerated(n_clicks, frequency, holidayDropdown, holidayScale, seasonalityScale, changepointScale, seasonalityMode, contents, filename, paramSearch):
    print(n_clicks, frequency, holidayDropdown, holidayScale, seasonalityScale, changepointScale, seasonalityMode, filename, paramSearch)
    if n_clicks is not None:
        try:
            df = parseContents(contents, filename)
            generateModel(frequency, holidayDropdown, holidayScale, seasonalityScale, changepointScale, seasonalityMode, df, paramSearch)
        except Exception as e:
            return 'Failure'
        return 'Notify'
    return 'VOID'


@cache.memoize()
def generateModel(freq, holidayDropdown, holidayScale, seasonalityScale, changepointScale, seasonalityMode, df, paramSearch):
    if paramSearch is not None and 1 in paramSearch:
        return generateParamSearchModel(df, frequency, holidayDropdown)
    df.columns = ['ds', 'y']
    df['ds'] = pd.to_datetime(df['ds'], dayfirst = True)
    df.sort_values(by = ['ds'])
    df.dropna(axis =0, how='any', inplace=True)
    df = df.reset_index(drop=True)
    model = Prophet(holidays_prior_scale = holidayScale, seasonality_prior_scale = seasonalityScale, changepoint_prior_scale = changepointScale, seasonality_mode = seasonalityMode)
    if freq in ['D', 'W', 'M', 'Q']:
        model.add_seasonality(name = 'monthly', period = 30.5, fourier_order = 5)
        model.add_seasonality(name = 'quarterly', period = 91.3, fourier_order = 7)
    if holidayDropdown is not None and holidayScale > 0:
        model.add_country_holidays(country_name = holidayDropdown)
    model.fit(df)
    print('#################### Model Trained #######################')
    return model


