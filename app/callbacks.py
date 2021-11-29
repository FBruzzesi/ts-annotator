from copy import copy
import dash
from dash import dash_table
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import yaml

from app import app
from utils import create_result_table, parse_contents, path_to_coords, ray_casting_2d
from utils import Point, Edge, Poly

with open('config.yaml') as config_file:
    configs = yaml.load(config_file, Loader=yaml.Loader)
    
colors = configs['colors']
# graph_config = configs['graph_config']


@app.callback(
    Output("graph-pic", "figure"),
    Input({"type": "label-color-button", "index": ALL}, "n_clicks_timestamp"),
    State("graph-pic", "figure"),
    prevent_initial_call=True,
)
def on_color_change(color_idx, figure):
    """Changes color of the shape to draw in the graph"""
    
    if color_idx is None: _idx = 0
    else:
        _idx = max(
            enumerate(color_idx),
            key=lambda t: 0 if t[1] is None else t[1],
        )[0]

    color = colors[_idx]
    figure["layout"]['newshape'] = {"line": {"color": color, "width": 3}}

    return figure


@app.callback(
    [Output("table", "children"),
     Output("data-store", "data"),
     Output("data-loader", "children"),
     Output("x-col", "options"),
     Output("y-col", "options")],
    [Input("data-loader", "contents"),
     Input("graph-pic", "relayoutData")],
    [State("data-loader", "filename"),
     State("data-store", "data"),
     State("label", "value"),
     State("data-loader", "children"),
     State("x-col", "options")],
    prevent_initial_call=True,
)
def on_upload_or_annotation(contents, relayout_data, filename, df_jsonified, label, msg, orig_col_options):
    """labels data inside new annotation"""
    
    ctx = dash.callback_context

    # Check what triggered the update
    if not ctx.triggered: return dash.no_update
    else: trigger = ctx.triggered[0]['prop_id'].split('.')[0]


    if trigger == "data-loader":
        
        df, msg = parse_contents(contents, filename)
        col_options = [{'label': c, 'value': c} for c in df.columns]
        return None, df.to_json(date_format='iso', orient='split'), msg, copy(col_options), copy(col_options)


    elif trigger == "graph-pic":
        
        dff = pd.read_json(df_jsonified, orient='split')
        
        shapes = relayout_data.get("shapes")
        shape = shapes[-1]
        shape_type = shape.get("type")
        
        # Closed Path
        if shape_type == 'path': 

            coords = path_to_coords(shape.get("path"))

            poly = Poly(
                name='closed_shape', 
                edges = tuple([
                    Edge(a=Point(x=x0, y=y0), b=Point(x=x1, y=y1)) for (x0, y0), (x1, y1) in zip(coords[:-1], coords[1:])]
                    )
                )
            msk = dff.apply(lambda row: ray_casting_2d(Point(row['x'], row['y']), poly), axis=1)
        
        # Rect
        else: 
            x0, y0, x1, y1 = shape.get("x0"), shape.get("y0"), shape.get("x1"), shape.get("y1")

            if x0 > x1: x0, x1 = x1, x0
            if y0 > y1: y0, y1 = y1, y0

            msk = (dff['x'].between(x0, x1)) & (dff['y'].between(y0, y1))
        

        dff.loc[msk, 'label'] = label
        dfj = dff.to_json(date_format='iso', orient='split')
        result_dt = create_result_table(dff)

        return result_dt, dfj, msg, copy(orig_col_options), copy(orig_col_options)
    
    else:
        return dash.no_update
