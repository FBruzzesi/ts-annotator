# PyPi imports
import base64, io, sys
from collections import namedtuple
from typing import Dict

import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import yaml

from dash import dcc, html, dash_table
from numba import jit
from pandas.api.types import is_numeric_dtype as is_numeric

# Load config file
with open("config.yaml") as config_file:
    configs = yaml.safe_load(config_file)

xtype_to_mode = configs["xtype_to_mode"]
table_style = configs["table_style"]
graph_layout = configs["graph_layout"]


def path_to_coords(svg_path: str, xtype: str = None) -> np.array:
    """From SVG path to numpy array of coordinates, each row being a (row, col) point"""
    indices_str = [
        pt.replace("M", "").replace("Z", "").replace("_", " ").split(",") for pt in svg_path.split("L")
    ]
    if xtype == "datetime":
        indices_str = [[dt_series_to_unix(pd.to_datetime(e[0])), float(e[1])] for e in indices_str]

    return np.array(indices_str, dtype=float)


def parse_contents(contents, filename):
    """Parse '.csv' or '.xls' file"""

    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    default_df = pd.DataFrame()
    default_msg = "There was a problem with the file"

    if "csv" in filename:
        # Assume that the user uploaded a CSV file
        try:
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            return df, f"Loaded {filename} successfully"

        except: return default_df, default_msg

    elif "xls" in filename:
        # Assume that the user uploaded an excel file
        try:
            df = pd.read_excel(io.BytesIO(decoded))
            return df, f"Loaded {filename} successfully"

        except: return default_df, default_msg

    else:
        return default_df, "Make sure format is 'csv' or 'xlsx'"


def check_col_type(s: pd.Series) -> str:
    """Checks pd.Series dtype"""

    if is_numeric(s):
        return "numeric"
    else:
        try:
            pd.to_datetime(s)
            return "datetime"

        except:
            return "categorical"


def make_figure(df: pd.DataFrame, xcol: str, ycol: str) -> go.Figure:
    """Generate different kind of figures based on x-axis dtype"""

    xtype = check_col_type(df[xcol])
    ytype = check_col_type(df[ycol])

    assert xtype in ["numeric", "datetime"]
    assert ytype == "numeric"

    if xtype == "datetime":
        df[xcol] = pd.to_datetime(df[xcol])

    figure = go.Figure(
        go.Scattergl(
            x = df[xcol],
            y = df[ycol],
            mode = xtype_to_mode[xtype],
            marker = {
                "line": {
                    "width": 1,
                    "color": "DarkSlateGrey"
                    }
                }
            )
        )

    figure.update_layout(
        xaxis_title=xcol,
        yaxis_title=ycol,
        **graph_layout
        )

    return figure


def dt_series_to_unix(s: pd.Series) -> pd.Series:
    """Converts datetime series to unix int"""

    try:
        s = pd.to_datetime(s)
        return (s - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")

    except:
        raise TypeError


def assign_label_mask(df: pd.DataFrame, xcol: str, ycol: str, shape: Dict[str, str]):
    """Assign label from given annotation"""
    shape_type = shape.get("type")
    xtype = check_col_type(df[xcol])

    # Closed Path
    if shape_type == "path":

        coords = path_to_coords(shape.get("path"), xtype=xtype)

        poly = Poly(
            name="closed_shape",
            edges = tuple([
                Edge(a=Point(x=x0, y=y0), b=Point(x=x1, y=y1)) for (x0, y0), (x1, y1) in zip(coords[:-1], coords[1:])]
                )
            )

        xtype = check_col_type(df[xcol])

        xnew = "x_tmp"
        df[xnew] = dt_series_to_unix(df[xcol]) if xtype == "datetime" else df[xcol]
        msk = df.apply(lambda row: ray_casting_2d(Point(row[xnew], row[ycol]), poly), axis=1)
        df.drop(xnew, axis=1, inplace=True)

    # Rect
    else:
        x0, y0, x1, y1 = shape.get("x0"), shape.get("y0"), shape.get("x1"), shape.get("y1")

        if x0 > x1: x0, x1 = x1, x0
        if y0 > y1: y0, y1 = y1, y0

        msk = (df[xcol].between(x0, x1)) & (df[ycol].between(y0, y1))

    return msk


def create_result_card(df: pd.DataFrame, xcol: str, ycol: str) -> dbc.Col:
    """Generates Card for resulting table"""

    fixed_cols = [xcol, ycol, "label"]

    result_dt = dash_table.DataTable(
            data = df.loc[:, fixed_cols].to_dict("records"),
            id = "result-table",
            columns = [{"name": c, "id": c} for c in fixed_cols],
            fixed_rows = {"headers": True, "data": 0},
            style_header = table_style["header"],
            style_table = {
                    "height": table_style["table_height"],  # 20 rows
                    "minHeight": table_style["table_height"],
                    "maxHeight": table_style["table_height"],
                    "overflowY": "auto",
            },
            style_cell = {
                "minWidth": table_style["cell_width"],
                "maxWidth": table_style["cell_width"],
                "width": table_style["cell_width"],
            },
            style_data = table_style["data"],
            style_data_conditional = [{"if": {"row_index": "odd"}, "backgroundColor": "rgb(220, 220, 220)"}],
            page_current = 0,
            page_size = 250,
            page_count = 0,
            page_action = "custom",
            virtualization = True,
        )

    result_card = dbc.Card(
        id="result-card",
        children=[
            dbc.CardHeader("Results"),
            dbc.CardBody(
                children=[
                    dbc.Button(
                        children=[
                            html.I(className="bi bi-cloud-download"),
                            " Download Results"
                            ],
                        id="btn-download-results",
                        color="success",
                        className="mt-auto",
                        style={"margin-bottom": "10px"}
                    ),
                    result_dt,
                    dcc.Download(id="download-dataframe-csv")
            ])
        ])

    return result_card


# Implementation of ray-casting algorithm from https://rosettacode.org/wiki/Ray-casting_algorithm#Python

Point = namedtuple('Point', 'x, y')      # Point
Edge = namedtuple('Edge', 'a, b')        # Polygon edge from a to b
Poly = namedtuple('Poly', 'name, edges') # Polygon

_eps = 0.00000001
_huge = sys.float_info.max
_tiny = sys.float_info.min


@jit(fastmath=True)
def rayintersectseg(p: Point, edge: Edge) -> bool:
    """Takes a point p=Point() and an edge of two endpoints a=Point(), b=Point() of a line segment returns boolean"""

    a, b = edge

    if a.y > b.y:
        a, b = b, a

    if (p.y == a.y) or (p.y == b.y):
        p = Point(p.x, p.y + _eps)


    if (p.y > b.y or p.y < a.y) or (p.x > max(a.x, b.x)):
        intersect = False

    elif p.x < min(a.x, b.x):
        intersect = True

    else:
        if abs(a.x - b.x) > _tiny:
            m_red = (b.y - a.y) / float(b.x - a.x)
        else:
            m_red = _huge
        if abs(a.x - p.x) > _tiny:
            m_blue = (p.y - a.y) / float(p.x - a.x)
        else:
            m_blue = _huge

        intersect = m_blue >= m_red

    return intersect


@jit(fastmath=True)
def _odd(x: int) -> bool:
    """Checks if integer is odd"""
    return x%2 == 1


@jit(fastmath=True)
def ray_casting_2d(p: Point, poly: Poly) -> bool:
    """Implements ray-casting algorithm to check if a point p is inside a (closed) polygon poly"""
    intersections = [int(rayintersectseg(p, edge)) for edge in poly.edges]
    return _odd(sum(intersections))
