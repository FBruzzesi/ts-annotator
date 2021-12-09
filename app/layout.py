# PyPi imports
from dash import html, dcc
import dash_bootstrap_components as dbc
import yaml
import plotly.graph_objects as go

# Load config file
with open('config.yaml') as config_file:
    configs = yaml.safe_load(config_file)
    
colors = configs['colors']
graph_config = configs['graph_config']

# Initialize empty figure
figure = go.Figure()

figure.update_layout(
    height=450,
    margin=dict(l=80, r=30, t=50, b=50),
    xaxis_title="x-axis",
    yaxis_title="y-axis",
    dragmode="drawrect",
    template="seaborn",
    newshape={"line": {"color": "indianred", "width": 2}}
    )


# Header Container
header = dbc.Container(
    id='app-header',
    fluid=True,
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[html.Div([html.H3(["Time Series Annotator App ", html.I(className="bi bi-pencil-square")])], id="app-title")],
                    align="center",
                    width={"offset": 4},
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
                    html.H6([html.I(className="bi bi-cloud-upload"), " Load Data"], className="card-title"),
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
                                    html.H6([html.I(className="bi bi-arrow-left-right"), " Select x-axis"], className="card-title"),
                                    dcc.Dropdown(id='x-col')
                                    ]),
                                dbc.Col([
                                    html.H6([html.I(className="bi bi-arrow-down-up"), " Select y-axis"], className="card-title"),
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
                    html.H6([html.I(className="bi-pencil"), " Label Value"], className="card-title"),
                    dcc.Input(id="label"),
                    html.Hr(),
                    html.H6([html.I(className="bi-palette"), " Select Color"], className="card-title"),
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
            dcc.Graph(id="graph-pic", figure=figure, config=graph_config)
            ]
        ) 

data_store = dcc.Store(id="data-store")


# Github link button
github = dbc.Button(
    [html.I(className="bi bi-github"), " Github"],
    outline=True,
    href="https://github.com/FBruzzesi/ts-annotator",
    id="gh-link",
    external_link=True,
    style={"text-transform": "none"},
)
# Report a Bug link button
report_bug = dbc.Button(
    [html.I(className="bi bi-bug-fill"), " Report a Bug"],
    outline=True,
    href="https://github.com/FBruzzesi/ts-annotator/issues",
    id="bug-link",
    external_link=True,
    style={"text-transform": "none"},
)



# Linkedin link button
linkedin = dbc.Button(
    [html.I(className="bi bi-linkedin"), " Linkedin"],
    outline=True,
    href="https://linkedin.com/in/francesco-bruzzesi/",
    id="linkedin-link",
    external_link=True,
    style={"text-transform": "none"},
)
# StackOverflow link button
stackoverflow = dbc.Button(
    [html.I(className="bi bi-stack"), " Stackoverflow"],
    outline=True,
    href="https://stackoverflow.com/users/12411536/fbruzzesi",
    id="so-link",
    external_link=True,
    style={"text-transform": "none"},
)

# Support link button
support = dbc.Button(
    [html.I(className="bi bi-cup-fill"), " Buy me a coffee"],
    outline=True,
    href="https://ko-fi.com/francescobruzzesi",
    id="support-link",
    external_link=True,
    style={"text-transform": "none"},
)

social_container = dbc.Container(
    id="social",
    children=[
        github,
        report_bug,
        linkedin,
        stackoverflow,
        support]
)