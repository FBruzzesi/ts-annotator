import base64, io, sys
from collections import namedtuple

import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

from numba import jit

def path_to_coords(svg_path: str) -> np.array:
    """From SVG path to numpy array of coordinates, each row being a (row, col) point"""
    indices_str = [
        pt.replace("M", "").replace("Z", "").split(",") for pt in svg_path.split("L")
    ]
    return np.array(indices_str, dtype=float)


def parse_contents(contents, filename):
    """Parse '.csv' or '.xls' file"""
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return df, f'Loaded {filename} successfully'

        except:
            return pd.DataFrame(), 'There was a problem with the file'
    
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        try:
            df = pd.read_excel(io.BytesIO(decoded))
            return df, f'Loaded {filename} successfully'

        except:
            return pd.DataFrame(), 'There was a problem with the file'
    else:
        return pd.DataFrame(), "Make sure format is 'csv' or 'xlsx'"



def create_result_table(df: pd.DataFrame):
    """Generates Card for resulting table"""
    result_dt = dbc.Col([
        dbc.Card(
            id='result-card',
            children=[
                dbc.CardHeader("Results"),
                dbc.CardBody(
                    dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True))
            ]),
        ])

    return result_dt



# Implementation of ray-casting algorithm from https://rosettacode.org/wiki/Ray-casting_algorithm#Python

Point = namedtuple('Point', 'x, y')      # Point
Edge = namedtuple('Edge', 'a, b')        # Polygon edge from a to b
Poly = namedtuple('Poly', 'name, edges') # Polygon
 
_eps = 0.00000001
_huge = sys.float_info.max
_tiny = sys.float_info.min

@jit
def rayintersectseg(p: Point, edge: Edge) -> bool:
    """Takes a point p=Point() and an edge of two endpoints a=Point(), b=Point() of a line segment returns boolean"""
    a, b = edge
    if a.y > b.y:
        a, b = b, a
    
    if (p.y == a.y) or (p.y == b.y): 
        p = Point(p.x, p.y + _eps)
 
    intersect = False
 
    if (p.y > b.y or p.y < a.y) or (p.x > max(a.x, b.x)):
        return False
 
    if p.x < min(a.x, b.x):
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

@jit
def _odd(x: int) -> bool:
    return x%2 == 1

@jit
def ray_casting_2d(p: Point, poly: Poly) -> bool:
    """Implements ray-casting algorithm to check if a point p is inside a (closed) polygon poly"""
    intersections = [int(rayintersectseg(p, edge)) for edge in poly.edges]
    return _odd(sum(intersections))