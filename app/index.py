from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np
import pandas as pd
import yaml

from app import app
import callbacks
from layout import header, sidebar

with open('colors.yaml') as color_file:
    colors = yaml.load(color_file, Loader=yaml.Loader)['colors']


size = 20
x = np.arange(0, size)
y = np.random.randn(size)

df = pd.DataFrame({'x': x, 'y': y})

fig = px.scatter(data_frame=df, x="x", y="y")
fig.update_layout(
    dragmode="drawrect",
    newshape={"line": {"color": "indianred", "width": 2}}
    )

config = {
    "modeBarButtonsToAdd": [
        "drawclosedpath",
        "drawcircle",
        "drawrect",
        # "eraseshape",
    ]
}


app.layout = html.Div(
    id="layout",
    children=[
        header,
        dbc.Container(
            dbc.Col(sidebar, md=2),
            fluid=True),
        # dcc.Textarea(id="label"),
        # dcc.Dropdown(
        #     id="color",
        #     options=[{'label': c.capitalize(), 'value':c } for c in colors],
        #     value='darkblue'
        # ),
        dcc.Store(id="ts-data", data=df.assign(label=np.nan).to_json(date_format='iso', orient='split')),
        dcc.Graph(id="graph-pic", figure=fig, config=config),
        html.Div(
            id="table",
            children=[dash_table.DataTable(id='tbl', data=df.to_dict('records'), columns=[{"name": i, "id": i} for i in df.columns])]
        )
    ]
)



if __name__ == "__main__":
    app.run_server(
        debug=True,
        port='8088',
        host='0.0.0.0'
    )
