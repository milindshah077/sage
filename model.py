from app import app
from dash.dependencies import Input,Output,State
from fbprophet import Prophet
import pandas as pd
from flask_caching import Cache
from utility import parseContents
import numpy as np
from sklearn.model_selection import ParameterGrid



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
            return str(e)
        return 'NOTIFY'
    return 'VOID'


@cache.memoize()
def generateModel(freq, holidayDropdown, holidayScale, seasonalityScale, changepointScale, seasonalityMode, df, paramSearch):
    if paramSearch is not None and 1 in paramSearch:
        return generateParamSearchModel(df, freq, holidayDropdown)
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


def generateParamSearchModel(df, freq, holidayDropdown):
    df.columns = ['ds', 'y']
    df['ds'] = pd.to_datetime(df['ds'], dayfirst = True)
    df.sort_values(by = ['ds'])
    df.dropna(axis =0, how='any', inplace=True)
    df = df.reset_index(drop=True)

    holidayScale = [10, 30, 50]
    seasonalityScale = [10, 30, 50]
    changepointScale = [0.1, 0.3, 0.5]
    mode = ['multiplicative', 'additive']
    paramGrid = {
        'seasonalityScale' : seasonalityScale,
        'changepointScale' : changepointScale,
        'mode' : mode
    }
    if holidayDropdown is not None:
        paramGrid['holidayScale'] = holidayScale
    
    grid = ParameterGrid(paramGrid)
    model_parameters = pd.DataFrame(columns = ['MAE', 'Parameters'])
    cnt = 1
    for p in grid:
        print(p)
        tmodel = Prophet(seasonality_prior_scale = p['seasonalityScale'], changepoint_prior_scale = p['changepointScale'], seasonality_mode = p['mode'])
        
        if holidayDropdown is not None:
            tmodel = Prophet(holidays_prior_scale = p['holidayScale'], seasonality_prior_scale = p['seasonalityScale'], changepoint_prior_scale = p['changepointScale'], seasonality_mode = p['mode'])
            tmodel.add_country_holidays(country_name = holidayDropdown)
        if freq in ['D', 'W', 'M', 'Q']:
            tmodel.add_seasonality(name = 'monthly', period = 30.5, fourier_order = 5)
            tmodel.add_seasonality(name = 'quarterly', period = 91.3, fourier_order = 7)
        tmodel.fit(df)
        future = tmodel.make_future_dataframe(periods = 0, freq = freq)
        forecast = tmodel.predict(future)
        forecast.sort_values(by = ['ds'])
        mae = mean_absolute_error(df['y'], forecast['yhat'])
        model_parameters = model_parameters.append({'MAE' : mae, 'Parameters' : p}, ignore_index = True)
        print('###################### MAE {} #########################'.format(cnt), mae)
        cnt+=1
    
    parameters = model_parameters.sort_values(by=['MAE'])
    parameters = parameters.reset_index(drop=True)
    print(parameters.head())
    finalp = parameters['Parameters'][0]
    print('Final Parameters ', finalp) 
    
    finalModel = Prophet(seasonality_prior_scale = finalp['seasonalityScale'], changepoint_prior_scale = finalp['changepointScale'], seasonality_mode = finalp['mode'])
    
    if holidayDropdown is not None:
        finalModel = Prophet(holidays_prior_scale = finalp['holidayScale'], seasonality_prior_scale = finalp['seasonalityScale'], changepoint_prior_scale = finalp['changepointScale'], seasonality_mode = finalp['mode'])
        finalModel.add_country_holidays(country_name = holidayDropdown)
    
    if freq in ['D', 'W', 'M', 'Q']:
        finalModel.add_seasonality(name = 'monthly', period = 30.5, fourier_order = 5)
        finalModel.add_seasonality(name = 'quarterly', period = 91.3, fourier_order = 7)
    
    finalModel.fit(df)
    print('#################### Suitable Model Trained #######################')
    return finalModel


def mean_absolute_error(y, yhat):
    y, yhat = np.array(y), np.array(yhat)
    return np.mean(np.abs(y - yhat))



