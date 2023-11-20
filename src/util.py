import dash                              # pip install dash
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
from dash_extensions import Lottie       # pip install dash-extensions
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
import plotly.express as px              # pip install plotly
import pandas as pd                      # pip install pandas
from datetime import date
import calendar 
from src.data import*

#components of first row and first column
card=dbc.Card([dbc.CardImg(src='/assets/linkedin-logo2.png')],className='mb-2') 
card_link=dbc.Card([dbc.CardBody([dbc.CardLink("Charming Data", target="_blank",href="https://youtube.com/charmingdata")])])

#components of first row and 2nd column
date_picker=dbc.Card([dbc.CardBody([
                    html.H6("Select Date",className="card-title",style={"text-align": "center"}),
                    html.Div([dcc.DatePickerSingle(
                        id='my-date-picker-start',
                        date=date(2018, 1, 1),
                        className='ml-auto mr-auto'),

                        dcc.DatePickerSingle(
                        id='my-date-picker-end',
                        date=date(2021, 4, 4),
                        className='ml-auto')], style={"text-align":"center"}),])],color='info', style={'height':'18vh'}) 
#Height of the card will be 18% of the height of the viewport.
#Html.div acts as a container. By using html.div i was able to align 2 date pickers at center.
#Html components can be written inside card body
#All about card: https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/
#card has header and body #we can adjust both height & width of the card
connection_card=dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="67%", height="67%", url=url_coonections)),
                dbc.CardBody([
                    html.H6('Connections'),
                    html.H2(id='content-connections', children=[])
                ], style={'textAlign':'center'})
            ])

company_card=dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="32%", height="32%", url=url_companies)),
                dbc.CardBody([
                    html.H6('Companies'),
                    html.H2(id='content-companies', children="000")
                ], style={'textAlign':'center'})
            ])

invite_received_card=dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_msg_in)),
                dbc.CardBody([
                    html.H6('Invites received'),
                    html.H2(id='content-msg-in', children="000")
                ], style={'textAlign':'center'})
            ])

invite_sent_card=dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="53%", height="53%", url=url_msg_out)),
                dbc.CardBody([
                    html.H6('Invites sent'),
                    html.H2(id='content-msg-out', children="000")
                ], style={'textAlign': 'center'})
            ])

reaction_card=dbc.Card([
                dbc.CardHeader(Lottie(options=options, width="25%", height="25%", url=url_reactions)),
                dbc.CardBody([
                    html.H6('Reactions'),
                    html.H2(id='content-reactions', children="000")
                ], style={'textAlign': 'center'})
            ])

linechart_card=dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='line-chart', figure={}, config={'displayModeBar': False}),
                ])
            ])

barchart_card=dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='bar-chart', figure={}, config={'displayModeBar': False}),
                ])
            ])



            