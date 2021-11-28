import dash
from dash import dash_table
from dash.dependencies import Input, Output, State, ALL
import pandas as pd

from app import app

colors = ["indianred", "seagreen", "mediumblue", "goldenrod"]

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
     Output("ts-data", "data")],
    [Input("graph-pic", "relayoutData")],
    [State("ts-data", "data"),
     State("label", "value")],
    prevent_initial_call=True,
)
def on_new_annotation(relayout_data, df_jsonified, label):
    """labels data inside new annotation"""
    
    shapes = relayout_data.get("shapes")

    if shapes:
        
        dff = pd.read_json(df_jsonified, orient='split')
        
        shape = shapes[-1]

        x0, y0, x1, y1 = shape.get("x0"), shape.get("y0"), shape.get("x1"), shape.get("y1")

        if x0 > x1: x0, x1 = x1, x0
        if y0 > y1: y0, y1 = y1, y0
        
        msk = (dff['x'].between(x0, x1)) & (dff['y'].between(y0, y1))
        dff.loc[msk, 'label'] = label

        dfj = dff.to_json(date_format='iso', orient='split')
        dt = dash_table.DataTable(id='tbl', data=dff.to_dict('records'), columns=[{"name": i, "id": i} for i in dff.columns])
        return dt, dfj
    
    else:
        return dash.no_update
