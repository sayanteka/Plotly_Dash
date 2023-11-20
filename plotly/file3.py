import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
#from pandas_datareader import web
import datetime

start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2020, 12, 3)
df = web.DataReader(['AMZN','GOOGL','FB','PFE','MRNA','BNTX'],
                    'stooq', start=start, end=end)
df = df.stack().reset_index()
df.rename(columns={'level_0': 'Date'}, inplace=True)
#To render app at the same width and scale as the device screen.
#https://hackerthemes.com/bootstrap-cheatsheet/ : bootstrap cheatsheet
#
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H1("Stock Market Dashboard",
                        className='text-center text-primary mb-5'),
                width=12)) ,#width of the col is 12. Here first row is having one column. Also primary=colour, mb=4 margin is left at bottom, text assigned at center. Refer
                           #bootstrap for the same.
    dbc.Row([

        dbc.Col([
            dcc.Dropdown(id='my-dpdn', multi=False, value='AMZN',
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df['Symbols'].unique())],
                         ),
            dcc.Graph(id='line-fig', figure={})],width={'size':5, 'offset':1}),
        
        #2nd col
        dbc.Col([
            dcc.Dropdown(id='my-dpdn2', multi=True, value=['PFE','BNTX'],
                         options=[{'label':x, 'value':x}
                                  for x in sorted(df['Symbols'].unique())]),
            dcc.Graph(id='line-fig2', figure={})
        ],width={'size':5, 'offset':1})
        ]),
    dbc.Row([dbc.Col([html.P("Select Company Stock:"),dcc.Checklist(id='my-checklist', value=['FB', 'GOOGL', 'AMZN'],
                          options=[{'label':x, 'value':x}
                                   for x in sorted(df['Symbols'].unique())],labelStyle={'display': 'inline-block','margin-right': '10px'}
                          ), dcc.Graph(id='my-hist', figure={})],width={'size':5, 'offset':1})
                          ])

],fluid=True)

@app.callback(
    Output('line-fig2', 'figure'),
    Input('my-dpdn2', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    figln2 = px.line(dff, x='Date', y='Open', color='Symbols')
    return figln2

@app.callback(
    Output('line-fig', 'figure'),
    Input('my-dpdn', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols']==stock_slctd]
    figln = px.line(dff, x='Date', y='High')
    return figln
# Histogram
@app.callback(
    Output('my-hist', 'figure'),
    Input('my-checklist', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['Symbols'].isin(stock_slctd)]
    dff = dff[dff['Date']=='2020-12-03']
    fighist = px.histogram(dff, x='Symbols', y='Close')
    return fighist

if __name__=='__main__':
    app.run_server(debug=True)

