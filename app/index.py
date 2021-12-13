# PyPi imports
from dash import html

# Local imports
from app import app, server
import callbacks
from layout import header, annotate_row, table_row, data_store

# App layout
app.layout = html.Div(
    id="layout",
    children=[
        header,
        annotate_row,
        table_row,
        data_store,
    ]
)

if __name__ == "__main__":
    app.run_server(
        debug=True,
        port='8080',
        host='0.0.0.0'
    )
