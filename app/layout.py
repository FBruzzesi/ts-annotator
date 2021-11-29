from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import yaml
import pandas as pd
import numpy as np
import plotly.express as px

with open('config.yaml') as config_file:
    configs = yaml.load(config_file, Loader=yaml.Loader)
    
colors = configs['colors']
graph_config = configs['graph_config']

size = 20
x = np.arange(0, size)
y = np.random.randn(size)

df = pd.DataFrame({'x': x, 'y': y})

fig = px.line(data_frame=df, x="x", y="y")

fig.update_layout(
    dragmode="drawrect",
    newshape={"line": {"color": "indianred", "width": 2}}
    )


# Github link button
gh_link = dbc.Button(
    "View Source Code",
    outline=True,
    color="warning",
    href="https://github.com/FBruzzesi/ts-annotator",
    id="gh-link",
    style={"text-transform": "none"},
)

# Header Container
header = dbc.Container(
    id='app-header',
    fluid=True,
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[html.Div([html.H3("Time Series Annotator App")], id="app-title")],
                    align="center",
                    width={"offset": 4},
                    ),
                dbc.Col(
                    children=[dbc.NavItem(gh_link)],
                    align="center",
                    ),
                ],
            ),
        ],
    )


# description_md = """Interactive app for (tabular) data annotation.

#     - Load data as csv
#     - Select x and y column to plot
#     - Input label/target value
#     - Select data in the graph
# """

# # Description
# description = dbc.Col(
#     [
#         dbc.Card(
#             id="description-card",
#             children=[
#                 dbc.CardHeader("How does it work?!"),
#                 dbc.CardBody(
#                     [
#                         dbc.Row(
#                             [
#                                 dbc.Col(
#                                     dcc.Markdown(description_md),
#                                     md=True,
#                                 ),
#                             ]
#                         ),
#                     ]
#                 ),
#             ],
#         )
#     ],
#     md=3,
# )

# toolbar
toolbar = [
    dbc.Card(
        id="loader-card",
        children=[
            dbc.CardHeader("Data Tools"),
            dbc.CardBody(
                style={"justify": 'center', "align": 'center'},
                children=[
                    html.H6("Load Data", className="card-title"),
                    dcc.Upload(
                        id='data-loader',
                        children=['Drag and Drop or ', html.A('Select a File')],
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center'
                        }),
                    html.Hr(),
                    html.Div(
                        children=[
                            dbc.Row([
                                dbc.Col([
                                    html.H6("Select x axis", className="card-title"),
                                    dcc.Dropdown(id='x-col')
                                    ]),
                                dbc.Col([
                                    html.H6("Select y axis", className="card-title"),
                                    dcc.Dropdown(id='y-col')
                                    ]),

                            ]),
                        ]
                    )
                ])]),
        dbc.Card(
        id="labeler-card",
        children=[
            dbc.CardHeader("Annotation Tools"),
            dbc.CardBody(
                style={"justify": 'center', "align": 'center'},
                children=[
                    html.H6("Label Value", className="card-title"),
                    dcc.Input(id="label"),
                    html.Hr(),
                    html.H6("Select Color", className="card-title"),
                    html.Div(
                        id="label-color-button",
                        children=[
                            dbc.Button(
                                "",
                                id={"type": "label-color-button", "index": _idx},
                                style={"background-color": c},
                                size="lg",className="me-1"
                            )
                            for _idx, c in enumerate(colors)
                        ],
                        ),
                    ]
                ),
            ],
        ),
]

graph = dbc.Card(
        id='fig-card', 
        children=[
            dbc.CardHeader("Graph"),
            dcc.Graph(id="graph-pic", figure=fig, config=graph_config)
            ]
        ) 

data_store = dcc.Store(id="data-store", data=df.assign(label=np.nan).to_json(date_format='iso', orient='split'))

result_dt = dbc.Col([
            dbc.Card(
                id='result-card',
                children=[
                    dbc.CardHeader("Results"),
                    dbc.CardBody(
                        dbc.Table.from_dataframe(pd.DataFrame(), striped=True, bordered=True, hover=True))
                ]),
            ],
            )