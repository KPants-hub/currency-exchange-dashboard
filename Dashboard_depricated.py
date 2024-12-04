# Building Dashboards
# Building Dashboards
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# First, create the Dash app using dash.Dash()
app = dash.Dash()

logo_link = "https://i0.wp.com/blog.apilayer.com/wp-content/uploads/2024/01/Navigating-the-Currency-Universe-A-Global-Exchange-Rate-API-Perspective.png?resize=1140%2C694&ssl=1"

app.layout = html.Div([
    html.Img(src=logo_link,
             # Add margin to the logo
             style={'float':'left','width':'250px',
                    'margin':'2px'}),
    html.H1('Currency Exchange Rates (USD)')], style={'text-align': 'center', 'font-size': 10, 'margin':'10px'})

if __name__ == '__main__':
    app.run_server(debug=False, port=8028)

