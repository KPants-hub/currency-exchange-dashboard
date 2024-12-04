import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load Data
latest_rates = pd.read_csv('latest_rates_df.csv')  # Current exchange rates
historical_rates = pd.read_csv('historical_exchange_data.csv')  # Historical rates

# Initialize Dash app
app = dash.Dash(__name__)

# Define the conversion rate function
def get_conversion_rate(base_currency, target_currency, rates_df):
    print(f"Base Currency: {base_currency}, Target Currency: {target_currency}")
    try:
        if base_currency == target_currency:
            return 1.0  # Same currency conversion
        if target_currency == "USD":
            return 1 / rates_df.loc[rates_df['symbol'] == base_currency, 'exchange_rate'].values[0]
        if base_currency == "USD":
            return rates_df.loc[rates_df['symbol'] == target_currency, 'exchange_rate'].values[0]
        else:
            base_to_usd = 1 / rates_df.loc[rates_df['symbol'] == base_currency, 'exchange_rate'].values[0]
            target_to_usd = rates_df.loc[rates_df['symbol'] == target_currency, 'exchange_rate'].values[0]
            return target_to_usd * base_to_usd
    except Exception as e:
        print(f"Error in conversion calculation: {e}")
        return None





# App Layout
app.layout = html.Div([
    html.H1("Exchange Rates Dashboard", style={'text-align': 'center'}),

    # Dropdowns for Base and Target Currencies
    html.Div([
        html.Label("Select Base Currency:"),
        dcc.Dropdown(
            id='base-currency',
            options=[
                {'label': 'USD', 'value': 'USD'},
                {'label': 'INR', 'value': 'INR'},
                {'label': 'EUR', 'value': 'EUR'}
            ],
            value='USD'  # Default value
        ),
        html.Label("Select Target Currency:"),
        dcc.Dropdown(
            id='target-currency',
            options=[
                {'label': 'USD', 'value': 'USD'},
                {'label': 'INR', 'value': 'INR'},
                {'label': 'EUR', 'value': 'EUR'}
            ],
            value='INR'  # Default value
        ),
    ]),

    # Conversion and Graph Section
    html.Div([
        html.H3(id='conversion-result'),
        dcc.Graph(id='exchange-graph')
    ])
])



@app.callback(
    [Output('conversion-result', 'children'),
     Output('exchange-graph', 'figure')],
    [Input('base-currency', 'value'),
     Input('target-currency', 'value')]
)


def update_dashboard(base_currency, target_currency):
    try:
        if base_currency == target_currency:
            conversion_text = f"1 {base_currency} = 1.0 {target_currency}"
            # Create a flat graph
            fig = px.line(
                x=['2020-01-01', '2023-12-31'],  # Arbitrary date range
                y=[1.0, 1.0],
                title=f"{base_currency} to {target_currency} Exchange Rate Over Time",
                labels={'x': 'Date', 'y': 'Exchange Rate'}
            )
            return conversion_text, fig

        # Get the conversion rate
        rate = get_conversion_rate(base_currency, target_currency, latest_rates)
        if rate is None:
            raise ValueError("Conversion rate not found.")

        conversion_text = f"1 {base_currency} = {rate:.4f} {target_currency}"

        # Filter historical data
        if target_currency == "USD":
            filtered_data = historical_rates[historical_rates['currency'] == base_currency].copy()
            filtered_data['rate'] = 1 / filtered_data['rate']
            filtered_data['currency'] = target_currency
        else:
            filtered_data = historical_rates[historical_rates['currency'] == target_currency]

        if filtered_data.empty:
            raise ValueError(f"No historical data available for {target_currency}.")

        # Create the line chart
        fig = px.line(
            filtered_data,
            x='date',
            y='rate',
            title=f"{base_currency} to {target_currency} Exchange Rate Over Time",
            labels={'rate': 'Exchange Rate', 'date': 'Date'}
        )

        return conversion_text, fig

    except Exception as e:
        print(f"Error: {e}")
        return "Error in conversion", {}

# Run the App
if __name__ == '__main__':
    app.run_server(debug=True)
