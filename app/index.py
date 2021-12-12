# PyPi imports
import callbacks
import dash_bootstrap_components as dbc
from dash import html
from layout import annotate_row
from layout import data_store
from layout import header
from layout import table_row

from app import app
# Local imports

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
