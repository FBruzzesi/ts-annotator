from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

colors = ["indianred", "seagreen", "mediumblue", "goldenrod"]

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

# sidebar
sidebar = [
    dbc.Card(
        id="sidebar-card",
        children=[
            dbc.CardHeader("Toolbar"),
            dbc.CardBody(
                style={"justify": 'center', "align": 'center'},
                children=[
                    html.H6("Label Value", className="card-title"),
                    dcc.Textarea(id="label"),
                    html.Hr(),
                    html.H6("Select Color", className="card-title"),
                    # Label class chosen with buttons
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