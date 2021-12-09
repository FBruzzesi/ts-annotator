# PyPi imports
from copy import copy
import pandas as pd
import yaml
import dash
from dash import dcc
from dash.dependencies import Input, Output, State, ALL

# Local imports
from app import app
from utils import create_result_table, parse_contents, make_figure, assign_label_mask, check_col_type

# Load config file
with open('config.yaml') as config_file:
    configs = yaml.safe_load(config_file)

colors = configs['colors']


# Callbacks
@app.callback(
    Output("graph-pic", "figure"),
    [Input("x-col", "value"),
     Input("y-col", "value"),
     Input({"type": "label-color-button", "index": ALL}, "n_clicks_timestamp")],
    [State("data-store", "data"),
     State("graph-pic", "figure")],
    prevent_initial_call=True,
)
def on_axis_or_color_change(xcol, ycol, color_idx, df_jsonified, figure):
    """
    Depending on the trigger, either:
    - Changes the x and y axis of the figure
    - Changes the color of the shape to draw in the graph
    """

    ctx = dash.callback_context

    # Check what triggered the update
    if not ctx.triggered: return dash.no_update
    else: trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    # If x and y axis are selected
    if (trigger in ["x-col", "y-col"]) and (xcol is not None) and (ycol is not None):

        df = (pd.read_json(df_jsonified, orient='split')
                .loc[:, [xcol, ycol]]
            )

        figure = make_figure(df=df, xcol=xcol, ycol=ycol)

        figure.update_layout(
            dragmode="drawrect",
            newshape={"line": {"color": "indianred", "width": 2}}
            )
        return figure

    # If new color is selected
    elif "label-color-button" in trigger:

        if color_idx is None: _idx = 0
        else:
            _idx = max(
                enumerate(color_idx),
                key=lambda t: 0 if t[1] is None else t[1],
            )[0]

        color = colors[_idx]
        figure["layout"]['newshape'] = {"line": {"color": color, "width": 2}}

        return figure

    else:
        return dash.no_update


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
     State("x-col", "options"),
     State("x-col", "value"),
     State("y-col", "value")],
    prevent_initial_call=True,
)
def on_upload_or_annotation(contents, relayout_data, filename, df_jsonified, label, msg, orig_col_options, xcol, ycol):
    """
    Depending on the trigger:
    - Loads and parses the data loaded from a csv/xlsx
    - Labels data inside new annotation (Rect or Path)
    """

    ctx = dash.callback_context

    # Check what triggered the update
    if not ctx.triggered: return dash.no_update
    else: trigger = ctx.triggered[0]["prop_id"].split(".")[0]

    shapes = relayout_data.get("shapes")

    # Parses the loaded file
    if trigger == "data-loader":
        
        df, msg = parse_contents(contents, filename)
        cols_to_display = [key for key, value in df.apply(check_col_type).to_dict().items() if value != "categorical"]
        col_options = [{"label": c, "value": c} for c in cols_to_display]
        
        return None, df.to_json(date_format="iso", orient="split"), msg, copy(col_options), copy(col_options)

    # Labels data inside new annotation
    elif (trigger == "graph-pic") and (shapes is not None):

        df = pd.read_json(df_jsonified, orient="split")
        shape = shapes[-1]

        msk = assign_label_mask(df=df, xcol=xcol, ycol=ycol, shape=shape)

        df.loc[msk, "label"] = label
        dfj = df.to_json(date_format="iso", orient="split")

        result_dt = create_result_table(df[[xcol, ycol, "label"]])

        return result_dt, dfj, msg, copy(orig_col_options), copy(orig_col_options)

    else:
        return dash.no_update


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-download-results", "n_clicks"),
    State("data-store", "data"),
    prevent_initial_call=True,
)
def download_results(n_clicks, df_jsonified):
    """Download data as csv when clicked"""

    if n_clicks:
        df = pd.read_json(df_jsonified, orient="split")
        return dcc.send_data_frame(df.to_csv, "result_df.csv", index=False)
