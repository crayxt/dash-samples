import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.express as px

import pandas as pd
import numpy as np

df = ( pd.DataFrame(np.random.rand(1000,4).round(4) * 10, columns=['Depth', 'V1', 'V2', 'V3'])
        .eval("V1 = V1 * 10")
        .sort_values('Depth')
        .set_index('Depth')
        .stack()
        .reset_index()
        .rename({'level_1': 'Log', 0: 'Value'}, axis=1)
)

app = dash.Dash(__name__)

layout2 = html.Div([
        html.Div([
            html.P("Figure Height"),
            dcc.Dropdown(id='height', options=[{"label": v, "value": v} for v in [100, 250, 500, 1000, 2000]], value=100)
        ], style={"width" : "25vw"}),
        html.Div([
            dcc.Graph(id="graph", figure={})
        ], style={"overflow" : "auto", "height" : "90vh", "width" : "70vw"} ),
], style={"display" : "flex", "justify-content" : "stretch", "flex-wrap": "wrap"})

app.layout = layout2

@app.callback(
    Output("graph", "figure"), 
    [Input('height', 'value')])
def resize_figure(height):
    fig = px.line(df, x="Value", y="Depth", facet_col="Log", color="Log", height=height)
    fig.update_layout(height=int(height)*7)
    fig.update_yaxes(autorange = "reversed", dtick=100/height)
    fig.update_xaxes(matches=None)
    return fig

app.run_server(debug=True)
