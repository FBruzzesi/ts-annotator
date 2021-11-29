import base64, io
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc


def path_to_coords(path: str) -> np.array:
    """From SVG path to numpy array of coordinates, each row being a (row, col) point"""
    indices_str = [
        el.replace("M", "").replace("Z", "").split(",") for el in path.split("L")
    ]
    return np.array(indices_str, dtype=float)

def ray_casting_2d(position, coords):
    """Implements ray-casting algorithm to check if a point is inside a (closed) polygon
    
    Params
    ------
    position: tuple
        x,y coordinates to test
    coords: np.array
        (n, 2) coordinates of the polygon vertices
    """
    pass


def parse_contents(contents, filename):
    """Parse '.csv' or '.xls' file"""
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    
    df_none = pd.DataFrame()

    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return df, f'Loaded {filename} successfully'
        except:
            return df_none, 'There was a problem with the file'
    
    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        try:
            df = pd.read_excel(io.BytesIO(decoded))
            return df, f'Loaded {filename} successfully'
        except:
            return df_none, 'There was a problem with the file'
    else:
        return df_none, "Make sure format is 'csv' or 'xlsx'"



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