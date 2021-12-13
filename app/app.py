import dash
import dash_bootstrap_components as dbc
from flask import Flask

# Flask server
server = Flask(__name__)

# Dash app
app = dash.Dash(
    __name__,
    server=server,
    suppress_callback_exceptions=True,
    title='ts-annotator',
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
        # "assets/style.css"
        ],
)
