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
from wordcloud import WordCloud
from widges.util import *  
from widges.data import *

# Bootstrap themes by Ann: https://hellodash.pythonanywhere.com/theme_explorer
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
#At the end of the row there will be margin at bottom & top
app.layout = dbc.Container([dbc.Row([dbc.Col([card,card_link],width=2),dbc.Col([date_picker],width=8)], className='mb-2 mt-2'),
                            dbc.Row([dbc.Col([connection_card],width=2),dbc.Col([company_card],width=2),dbc.Col([invite_received_card],width=2),
                                    dbc.Col([invite_sent_card],width=2),dbc.Col([reaction_card],width=2)],className='mb-2 mt-2'),
                            dbc.Row([dbc.Col([linechart_card],width=6),dbc.Col([barchart_card],width=6)])
                            ],fluid=True) #container closing bracket

@app.callback(
    Output('content-connections','children'),
    Output('content-companies','children'),
    Output('content-msg-in','children'),
    Output('content-msg-out','children'),
    Output('content-reactions','children'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date')
)
def update_small_cards(start_date, end_date):
    # Connections
    dff_c = df_cnt.copy()
    dff_c = dff_c[(dff_c['Connected On']>=start_date) & (dff_c['Connected On']<=end_date)]
    conctns_num = len(dff_c)
    compns_num = len(dff_c['Company'].unique())
    # Invitations
    dff_i = df_invite.copy()
    dff_i = dff_i[(dff_i['Sent At']>=start_date) & (dff_i['Sent At']<=end_date)]
    # print(dff_i)
    in_num = len(dff_i[dff_i['Direction']=='INCOMING'])
    out_num = len(dff_i[dff_i['Direction']=='OUTGOING'])
    # Reactions
    dff_r = df_react.copy()
    dff_r = dff_r[(dff_r['Date']>=start_date) & (dff_r['Date']<=end_date)]
    reactns_num = len(dff_r)
    return conctns_num, compns_num, in_num, out_num, reactns_num

@app.callback(
    Output('line-chart','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_line(start_date, end_date):
    dff = df_cnt.copy()
    dff = dff[(dff['Connected On']>=start_date) & (dff['Connected On']<=end_date)]
    dff = dff[["month"]].value_counts()
    dff = dff.to_frame()
    print(dff.head(2))
    dff.reset_index(inplace=True)
    dff.rename(columns={'count': 'Total connections'}, inplace=True)
    print(dff)
    fig_line = px.line(dff, x='month', y='Total connections',
                  title="Total Connections by Month Name")
    fig_line.update_traces(mode="lines+markers", fill='tozeroy',line={'color':'blue'})
    fig_line.update_layout(margin=dict(l=20, r=20, t=30, b=20))

    return fig_line


# Bar Chart ************************************************************
@app.callback(
    Output('bar-chart','figure'),
    Input('my-date-picker-start','date'),
    Input('my-date-picker-end','date'),
)
def update_bar(start_date, end_date):
    dff = df_cnt.copy()
    dff = dff[(dff['Connected On']>=start_date) & (dff['Connected On']<=end_date)]

    dff = dff[["Company"]].value_counts().head(6)
    dff = dff.to_frame()
    dff.reset_index(inplace=True)
    dff.rename(columns={'count':'Total connections'}, inplace=True)
    # print(dff_comp)
    fig_bar = px.bar(dff, x='Total connections', y='Company', template='ggplot2',
                      orientation='h', title="Total Connections by Company")
    fig_bar.update_yaxes(tickangle=45)
    fig_bar.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    fig_bar.update_traces(marker_color='blue')

    return fig_bar




if __name__=='__main__':
    app.run_server(debug=True, port=8000)