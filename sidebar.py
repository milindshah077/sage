import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from app import app
from dash.dependencies import Input, Output, State
from utility import parseContents
from exceptions import FileNotSupported

SIDEBAR_STYLE = {
    'position' : 'fixed',
    'top' : '5rem',
    'left' : 0,
    'bottom' : 0,
    'width' : '16rem',
    'padding' : '2rem 0.5rem',
    'background-color' : '#f2f2f2',
    'overflow' : 'scroll',
    'font-size' : '14px'
}

sidebar = html.Div(
    [
        html.Div(
            [
                'Upload a file of ',
                html.A('this format', 
                    href = 'assets/format.csv', 
                    download = 'format.csv', 
                    style = {'text-decoration' : 'underline' })
            ],
            style = {
                'padding' : '1rem 0'
            }
        ),
        html.Div([
            dcc.Upload(
                id='file',
                children=html.Div([
                    dbc.Button('Select a File', color = 'primary')
                ]),
                multiple = False
            )
        ]),
        html.Div(id = 'preview'),
        
        html.Div(['What is the ', html.Span('Frequency', style = {'font-weight' : 'bold'}), ' of your data?'], style = {'padding-top' : '1rem'}),
        dcc.Dropdown(
            id = 'frequency',
            options = [
                {'label' : 'Hourly', 'value': 'H'},
                {'label' : 'Daily' , 'value' : 'D' },
                {'label' : 'Weekly' , 'value' : 'W'},
                {'label' : 'Monthly' , 'value' : 'M'},
                {'label' : 'Quarterly' , 'value' : 'Q'},
                {'label' : 'Yearly' , 'value' : 'A'}
            ],
            placeholder = 'Choose a frequency'
        ),
        
        html.Div([html.Span('Country Holiday: ', style = {'font-weight' : 'bold'}), 'Use a built in country specific holiday'], style = {'padding-top' : '1rem'}),
        dcc.Dropdown(
            id = 'holidayDropdown',
            options = [
                {'label' : 'India' , 'value' : 'IN' },
                {'label' : 'Canada' , 'value' : 'CA'},
                {'label' : 'China' , 'value' : 'CN'},
                {'label' : 'Japan' , 'value' : 'JP'},
                {'label' : 'United Kingdom' , 'value' : 'UK'},
                {'label' : 'United States' , 'value' : 'US'}
            ],
            placeholder = 'Choose a country'
        ),
        
        dcc.Checklist(
            id='paramSearch',
            options = [
                {'label' : ' Find suitable parameters for me', 'value' : 1}
            ],
            style = {
                'padding-top': '1rem', 'font-weight': 'bold'
            }
        ),
        
        html.Div([html.Span('Holiday Strength: ', style = {'font-weight' : 'bold'}), 'Increase to strengthen influence of holidays'], style = {'padding-top' : '1rem'}),
        dcc.Input(id= 'holidayScale', type='number', value =10, min = 0, max = 50, step = 1, debounce = True, style = {'width' : '80%'}),
       

        html.Div([html.Span('Seasonality Strength: ', style = {'font-weight' : 'bold'}), 'Increase to strengthen influence of seasonality'], style = {'padding-top' : '1rem'}),
        dcc.Input(id= 'seasonalityScale', type='number', value =10, min = 0, max = 50, step = 1, debounce = True, style = {'width' : '80%'}),
        
        
        html.Div([html.Span('Trend Changes Scale: ', style = {'font-weight' : 'bold'}), 'Increase to fit more flexible model'], style = {'padding-top' : '1rem'}),
        dcc.Input(id= 'changepointScale', type='number', value =0.1, min = 0, max = 1, step = 0.1, debounce = True, style = {'width' : '80%'}),
        

        html.Div([html.Span('Seasonality Mode: ', style = {'font-weight' : 'bold'}), 'Use multiplicative if seasonal/holiday effect increases with time'], style = {'padding-top' : '1rem'}),
        dcc.Dropdown(
            id = 'seasonalityMode',
            options = [
                {'label' : 'Additive' , 'value' : 'additive' },
                {'label' : 'Multiplicative' , 'value' : 'multiplicative'}
            ],
            placeholder = 'Choose a mode'
        ),


        #html.Div([html.Span('Monthly Seasonality Strength: ', style = {'font-weight' : 'bold'}), 'Increase to strengthen influence of monthly seasonality'], style = {'padding-top' : '1rem'}),
        #dcc.Input(id= 'monthlyScale', type='number', value =10, min = 0, max = 50, step = 1, debounce = True, style = {'width' : '80%'}),
        
        #html.Div([html.Span('Yearly Seasonality Strength: ', style = {'font-weight' : 'bold'}), 'Increase to strengthen influence of yearly seasonality'], style = {'padding-top' : '1rem'}),
        #dcc.Input(id= 'yearlyScale', type='number', value =10, min = 0, max = 50, step = 1, debounce = True, style = {'width' : '80%'}),

        dbc.Button('Submit', id = 'submit', color = 'primary', style = {'width' : '50%', 'margin-top' : '1rem', 'margin-left' : '25%'}, disabled = True, outline = True)
    ],
    style = SIDEBAR_STYLE
)


def getPreview(df, filename):
    #preview = df[:5]
    return html.Div([
        # html.H5('Preview'),
        html.Span(filename, style = {'font-weight' : 'bold'}),
        str(df.shape)
        #dash_table.DataTable(
        #    data = preview.to_dict('records'),
        #    columns = [{'name' : i, 'id' : i} for i in preview.columns]
        #),
    ])

def showError(msg):
    return html.Div(msg)

def checkFileContent(contents, filename): 
    if contents is not None:
        try:
            data = parseContents(contents, filename)
            #check if data is jsonable
            #json.dumps(data.to_dict('record'))
            return True, data
        except FileNotSupported as e:
            print(e)
            return False, e.message
        except Exception as e:
            print(e)
            return False, 'There wan an error processing the file'
    else:
        return False, 'No File'     
    
@app.callback(
    Output('preview', 'children'),
    [Input('file', 'contents')],
    [State('file', 'filename')])
def onUpload(contents, filename):
    if contents is not None:
        isValid, data  = checkFileContent(contents, filename)
        if isValid:
            return getPreview(data, filename)
        else:
            return showError(data)

@app.callback(
    [Output('submit','disabled'),
     Output('submit', 'outline')],
    [Input('file', 'contents'),
     Input('holidayScale', 'value'),
     Input('seasonalityScale', 'value'),
     Input('changepointScale', 'value'),
     Input('frequency', 'value'),
     Input('paramSearch', 'value'),
     Input('seasonalityMode', 'value')],
    [State('file', 'filename')]
)
def validate(contents, holidayScale, seasonalityScale, changepointScale, frequency, paramSearch, seasonalityMode, filename):
    print(holidayScale, seasonalityScale, changepointScale, frequency, paramSearch, seasonalityMode, filename)
    isValid, data  = checkFileContent(contents, filename)
    if isValid and frequency is not None:
        if paramSearch is not None and 1 in paramSearch:
            return False, False
        elif seasonalityScale is not None and changepointScale is not None and holidayScale is not None and seasonalityMode is not None:
            return False, False
        else:
            return True, True
    else:
        return True, True


@app.callback(
    [Output('seasonalityMode','options'),
     Output('holidayScale', 'disabled'),
     Output('seasonalityScale', 'disabled'),
     Output('changepointScale', 'disabled')],
    [Input('paramSearch', 'value')]
)
def validate(paramSearch):
    if paramSearch is not None  and 1 in paramSearch:
        return [
                {'label' : 'Additive' , 'value' : 'additive', 'disabled' : True },
                {'label' : 'Multiplicative' , 'value' : 'multiplicative', 'disabled' : True}
            ], True, True, True
    else:
        return [
                {'label' : 'Additive' , 'value' : 'additive' },
                {'label' : 'Multiplicative' , 'value' : 'multiplicative'}
            ], False, False, False


