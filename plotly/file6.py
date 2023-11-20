from dash import Dash, dcc, html, Input, Output,State
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = pd.read_csv("Berlin_crimes.csv")
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#Making graph card. Graph card has card body enclosed inside card. card body has 4 componets:html, button, popover,graph
#button id and popover target are same as popover opens up when button is clicked. 
#popover has 2 components one is popover header and other is popover body
#current state of popover i.e. is_open=false i.e. it is closed. It becomes open when someone clicks
#colour of the card is light
#It generates alert if no option is selected
alert = dbc.Alert("Please choose Districts from dropdown to avoid further disappointment!", color="danger",
                  dismissable=True)
graph_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Graffiti in Berlin 2012-2019", className="card-title", style={"text-align": "center"}),
                dbc.Button(
                    "About Berlin", id="popover-bottom-target", color="info"
                ),
                dbc.Popover(
                    [
                        dbc.PopoverHeader("All About Berlin:"),
                        dbc.PopoverBody(
                            "Berlin (/bɜːrˈlɪn/; German: [bɛʁˈliːn] is the capital and largest city of Germany by both area and population. Its 3,769,495 (2019) inhabitants make it the most populous city proper of the European Union. The city is one of Germany's 16 federal states. It is surrounded by the state of Brandenburg, and contiguous with Potsdam, Brandenburg's capital. The two cities are at the center of the Berlin-Brandenburg capital region, which is, with about six million inhabitants and an area of more than 30,000 km2, Germany's third-largest metropolitan region after the Rhine-Ruhr and Rhine-Main regions. (Wikipedia)"),
                    ],
                    id="popover",
                    target="popover-bottom-target",  # needs to be the same as dbc.Button id
                    placement="bottom", #can be done at bottom, top and so on
                    is_open=False,
                ),
                html.Br(),
                html.H6("Choose Berlin Districts:", className="card-text"),
                html.Div(id="the_alert", children=[]),
                dcc.Dropdown(id='district_chosen', options=[{'label': d, "value": d} for d in df["District"].unique()],
                             value=["Lichtenberg", "Pankow", "Spandau"], multi=True, style={"color": "#000000"}),
                html.Hr(), #line break after dropdown #In Hr line break is visisble but in Br line break not visible
                dcc.Graph(id='line_chart', figure={}),

            ]
        ),
    ],
    color="light",
)
# app.layout = html.Div([
#     dbc.Row([dbc.Col(image_card, width=3), dbc.Col(graph_card, width=8)], justify="around")
# ])
app.layout = html.Div([
    dbc.Row(dbc.Col( dbc.Col(graph_card, width=8)))
])

@app.callback(
    Output("popover", "is_open"),
    [Input("popover-bottom-target", "n_clicks")],
    [State("popover", "is_open")],
)
#input=clicks
#current state=false
#output=current state=True on click
def toggle_popover(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(
    [Output("line_chart", "figure"),
     Output("the_alert", "children")],
    [Input("district_chosen", "value")]
)
def update_graph_card(districts):
    if len(districts) == 0:
        return dash.no_update, alert #dash.no_update to avoid callback error
                                     #first output refers to figure component and 2nd output refers to children component
    else:
        df_filtered = df[df["District"].isin(districts)]
        df_filtered = df_filtered.groupby(["Year", "District"])[['Graffiti']].median().reset_index()
        fig = px.line(df_filtered, x="Year", y="Graffiti", color="District",
                      labels={"Graffiti": "Graffiti incidents (avg)"}).update_traces(mode='lines+markers')
        return fig, dash.no_update
    
    
if __name__ == "__main__":
    app.run_server(debug=True)