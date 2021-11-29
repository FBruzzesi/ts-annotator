from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

from app import app
import callbacks
from layout import header, toolbar, graph, data_store #description


app.layout = html.Div(
    id="layout",
    children=[
        header,
        data_store,
        dbc.Container([
            #  dbc.Row(description),
            dbc.Row(
                children=[
                    dbc.Col(toolbar, md=3),
                    dbc.Col(graph, md=9)
                    ]
                 )
            ],
            fluid=True),
        dbc.Container(id="table")
    ]
)



if __name__ == "__main__":
    app.run_server(
        debug=True,
        port='8088',
        host='0.0.0.0'
    )
