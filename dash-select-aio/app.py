#conda create -n dash-env python=3.9 pandas dash plotly openpyxl
#conda activate dash-env
#conda install -c conda-forge dash dash-bootstrap-components colorama


import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Dash, Input, Output, State, dcc, html

import pandas as pd
import numpy as np

# Prepare data
a = np.random.rand(60,2).round(4) * 100
b = np.tile(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'], 4)
df = pd.DataFrame(a, columns=["X", "Y"])
df['ID'] = b
df = df.sort_values(by=['ID', 'X'])
# End of data preparation

from aio_components import SelectWithMemoryAIO

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


chart1 = dbc.Card(
    [
        html.Label("Hold Shift/Ctrl to select multiple values"),
        dbc.Row(
            [
                dbc.Col([SelectWithMemoryAIO("", aio_id='aio1', select_props=dict(options=df['ID'].unique(), className="form-select", size=15, multiple=True)),
                         html.Label('Above field is hidden by default')
                        ], width=4),
                dbc.Col(dcc.Graph(id="graph1", figure={}), width=8),
            ]),
    ],
    body=True,
)

chart2 = dbc.Card(
    [
        html.Label("Standard dcc.Dropdown"),
        dbc.Row(
            [
                dcc.Dropdown([{'label': c, 'value': c} for c in df['ID'].unique()], id="plot2", multi=True),
                dbc.Col(dcc.Graph(id="graph2", figure={}), width=8),
            ]),
    ],
    body=True,
)

chart3 = dbc.Card(
    [
        html.Label("Standard dcc.Checbox"),
        dbc.Row(
            [
                dcc.Checklist(df['ID'].unique(), [], id="plot3", inline=True),
                dbc.Col(dcc.Graph(id="graph3", figure={}), width=8),
            ]),
    ],
    body=True,
)


app.layout = dbc.Container(
    [
        html.H2("Comparison of html Select, dcc Dropdown and dcc Checkboxes"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(chart1, id="chart1", width=4),
                dbc.Col(chart2, id="chart2", width=4),
                dbc.Col(chart3, id="chart3", width=4),
            ],
            align="top",
        ),
        html.P(id='placeholder')
    ],
    fluid=True,
)

@app.callback(
    Output('graph1', 'figure'),
    Input(SelectWithMemoryAIO.ids.storage('aio1'), 'value')
)
def plot1(val):
    val = val.split(",") if val else []
    if not val:
        return {}
    dff = df.loc[df.ID.isin(val)]
    fig = px.scatter(dff, x='X', y='Y', color='ID')
    #print(fig)
    return fig

@app.callback(
    Output('graph2', 'figure'),
    Input('plot2', 'value'),
)
def plot2(val):
    if not val:
        return {}
    print(val)
    dff = df.loc[df.ID.isin(val)]
    fig = px.scatter(dff, x='X', y='Y', color='ID')
    #print(fig)
    return fig

@app.callback(
    Output('graph3', 'figure'),
    Input('plot3', 'value'),
)
def plot3(val):
    if not val:
        return {}
    print(val)
    dff = df.loc[df.ID.isin(val)]
    fig = px.scatter(dff, x='X', y='Y', color='ID')
    #print(fig)
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
