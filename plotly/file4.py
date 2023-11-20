from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
#https://dashcheatsheet.pythonanywhere.com/
#Link for boot strap cheat sheets
df = px.data.tips()
days = df.day.unique()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
day_dropdown = dcc.Dropdown(
    id="dropdown",
    options=[{"label": x, "value": x} for x in days],
    value=days[0],
    clearable=False,
    className="mt-3 text-danger",
)

fake_dropdown = dbc.Select(
    id="fake-bootstrap-dropdown",
    options=[{"label": x, "value": x} for x in df.sex.unique()],
    value="",
    placeholder="Fake disconnected dropdown for tutorial purposes",
    className="bg-success mt-3 text-danger fw-bolder"
)
#colour works but depends on screen background
#first was not showing red 
#2nd one is showing 
app.layout = dbc.Container([html.Br(),
               html.Span("Utility Color", className="border border-secondary",style={"color": "black", "font-weight": "bold"}),
               #html.Br(),
               #Here p=padding, mt=2(margin at top),bg-background colour primary text=light(white),font-weight bold
               #background opacity
               html.Div("default", className="p-2 mt-2 bg-primary text-light text-center fw-bold rounded") ,
               #margin =m all sides
               html.Div("Utility Spacing", className="border m-3") , 
               dbc.Row([dbc.Col(day_dropdown, width=6),
        dbc.Col(fake_dropdown, width=6)])     
                            ])
#https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Bootstrap/Stying/Dash-Bootsrap5-styling.py
#Github code link
#html.br produces line break in text
if __name__ == "__main__":
    app.run_server(debug=True)