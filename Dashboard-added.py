import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load Data
latest_rates = pd.read_csv('latest_rates_df.csv')  # Current exchange rates
historical_rates = pd.read_csv('historical_exchange_data.csv')  # Historical rates
kpi_summary = pd.read_csv('kpi_summary.csv')  # KPI data

# Initialize Dash app
app = dash.Dash(__name__)

# Define the conversion rate function
def get_conversion_rate(base_currency, target_currency, rates_df):
    if base_currency == target_currency:
        return 1.0
    if target_currency == "USD":
        return 1 / rates_df.loc[rates_df['symbol'] == base_currency, 'exchange_rate'].values[0]
    if base_currency == "USD":
        return rates_df.loc[rates_df['symbol'] == target_currency, 'exchange_rate'].values[0]
    else:
        base_to_usd = 1 / rates_df.loc[rates_df['symbol'] == base_currency, 'exchange_rate'].values[0]
        target_to_usd = rates_df.loc[rates_df['symbol'] == target_currency, 'exchange_rate'].values[0]
        return target_to_usd * base_to_usd

# App Layout
app.layout = html.Div(style={
    'font-family': 'Arial, sans-serif',
    'background': 'linear-gradient(to bottom, #f0f8ff, #e6f7ff)',
    'padding': '10px'
}, children=[
    # Header Section
    html.Div([
        html.H1("Exchange Rates Dashboard", style={
            'text-align': 'center',
            'margin': '0',
            'padding': '10px',
            'font-size': '24px',
        }),
    ], style={'background-color': '#f8f9fa', 'padding': '10px', 'border-bottom': '2px solid #ddd'}),

    # Dropdowns and KPIs Section
    html.Div([
        html.Div([
            html.Label("Select Base Currency:", style={'font-weight': 'bold'}),
            dcc.Dropdown(
                id='base-currency',
                options=[
                    {'label': 'USD', 'value': 'USD'},
                    {'label': 'INR', 'value': 'INR'},
                    {'label': 'EUR', 'value': 'EUR'}
                ],
                value='USD'  # Default value
            ),
            html.Label("Select Target Currency:", style={'font-weight': 'bold', 'margin-top': '10px'}),
            dcc.Dropdown(
                id='target-currency',
                options=[
                    {'label': 'USD', 'value': 'USD'},
                    {'label': 'INR', 'value': 'INR'},
                    {'label': 'EUR', 'value': 'EUR'}
                ],
                value='INR'  # Default value
            ),
        ], style={
            'width': '30%',
            'padding': '15px',
            'background-color': '#ffffff',
            'border-radius': '8px',
            'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.1)',
            'margin': '10px'
        }),

        html.Div(id='kpi-section', style={
            'width': '30%',
            'padding': '15px',
            'background-color': '#ffffff',
            'border-radius': '8px',
            'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.1)',
            'margin': '10px',
            'text-align': 'center'
        }),
    ], style={'display': 'flex', 'justify-content': 'space-around', 'align-items': 'center'}),

    # Conversion and Graph Section
    html.Div([
        html.H3(id='conversion-result', style={'text-align': 'center', 'margin-top': '10px'}),
        dcc.Graph(id='exchange-graph', style={'height': '400px', 'margin': '0 auto'}),  # Reduced height
    ], style={'margin-top': '10px', 'padding-bottom': '10px'}),

    # Footer Section
    html.Div([
        html.P("Powered by Fixer.io API | Developed by Your Team", style={'text-align': 'center', 'color': '#777'})
    ], style={'background-color': '#f8f9fa', 'padding': '10px', 'border-top': '2px solid #ddd'})
])


@app.callback(
    [Output('conversion-result', 'children'),
     Output('exchange-graph', 'figure'),
     Output('kpi-section', 'children')],
    [Input('base-currency', 'value'),
     Input('target-currency', 'value')]
)
def update_dashboard(base_currency, target_currency):
    try:
        # Handle same-currency conversion
        if base_currency == target_currency:
            conversion_text = f"1 {base_currency} = 1.0 {target_currency}"
            fig = px.line(
                x=['2020-01-01', '2023-12-31'], y=[1.0, 1.0],
                title=f"{base_currency} to {target_currency} Exchange Rate Over Time",
                labels={'x': 'Date', 'y': 'Exchange Rate'}
            )
            kpi_display = html.Div("No KPIs available for same-currency conversions.")
            return conversion_text, fig, kpi_display

        # Get the conversion rate
        rate = get_conversion_rate(base_currency, target_currency, latest_rates)
        if rate is None:
            raise ValueError("Conversion rate not found.")

        conversion_text = f"1 {base_currency} = {rate:.4f} {target_currency}"

        # Handle historical data for USD dynamically
        if target_currency == "USD":
            filtered_data = historical_rates[historical_rates['currency'] == base_currency].copy()
            filtered_data['rate'] = 1 / filtered_data['rate']
            filtered_data['currency'] = target_currency

            # Calculate KPIs dynamically for USD
            high = filtered_data['rate'].max()
            low = filtered_data['rate'].min()
            fluctuation = high - low

            kpi_display = html.Div([
                html.H4("Key Performance Indicators (KPIs):"),
                html.Div(f"High: {high:.4f}", style={'background-color': '#dff0d8', 'padding': '5px',
                                                     'margin-bottom': '5px', 'border-radius': '5px'}),
                html.Div(f"Low: {low:.4f}", style={'background-color': '#f2dede', 'padding': '5px',
                                                   'margin-bottom': '5px', 'border-radius': '5px'}),
                html.Div(f"Fluctuation: {fluctuation:.4f}", style={'background-color': '#d9edf7', 'padding': '5px',
                                                                   'border-radius': '5px'}),
            ])
        else:
            # Fetch KPIs for other currencies
            filtered_data = historical_rates[historical_rates['currency'] == target_currency]
            kpi_data = kpi_summary[kpi_summary['currency'] == target_currency]

            if not kpi_data.empty:
                high = kpi_data['max_rate'].values[0]
                low = kpi_data['min_rate'].values[0]
                fluctuation = kpi_data['fluctuation'].values[0]
                kpi_display = html.Div([
                    html.H4("Key Performance Indicators (KPIs):"),
                    html.Div(f"High: {high:.4f}", style={'background-color': '#dff0d8', 'padding': '5px',
                                                         'margin-bottom': '5px', 'border-radius': '5px'}),
                    html.Div(f"Low: {low:.4f}", style={'background-color': '#f2dede', 'padding': '5px',
                                                       'margin-bottom': '5px', 'border-radius': '5px'}),
                    html.Div(f"Fluctuation: {fluctuation:.4f}", style={'background-color': '#d9edf7', 'padding': '5px',
                                                                       'border-radius': '5px'}),
                ])
            else:
                kpi_display = html.Div("No KPI data available.")

        # Create the line chart
        fig = px.line(
            filtered_data,
            x='date',
            y='rate',
            title=f"{base_currency} to {target_currency} Exchange Rate Over Time",
            labels={'rate': 'Exchange Rate', 'date': 'Date'}
        )

        return conversion_text, fig, kpi_display

    except Exception as e:
        print(f"Error: {e}")
        return "Error in conversion", {}, html.Div("Error displaying KPIs.")


# Run the App
if __name__ == '__main__':
    app.run_server(debug=True)
