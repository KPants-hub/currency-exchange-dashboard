# Refined_Final_Project.py
# This file contains an improved version of the original code with more comments
# and functionality additions.

# Import required libraries
import requests  # For making API calls
import datetime  # For handling date-related tasks
from datetime import datetime
import pandas as pd  # For creating and manipulating data structures like DataFrame

# Set up API key
apikey = '7bf403592be68c3af0287ed3ab4a19ac'  # Replace with your actual API key

# Define function to retrieve the latest exchange rates
def fetch_latest_rates(api_key):
    """
    Fetches the latest exchange rates from the Fixer.io API.

    Parameters:
        api_key (str): API key for authentication.

    Returns:
        pd.DataFrame: A DataFrame containing the latest exchange rates.
    """
    url = 'http://data.fixer.io/api/latest'
    querystring = {"access_key": api_key, "base": "USD"}

    # Make the API call
    response = requests.get(url, params=querystring)
    response_json = response.json()

    # Debugging: Print the full JSON response
    print("Full JSON Response:")
    print(response_json)

    # Extract exchange rates
    latest_rate_values = response_json.get('rates', {})
    if not latest_rate_values:
        print("\nError: No rates data found in the response.")
        return None

    # Convert the currency symbols and their exchange rates into lists
    symbols = list(latest_rate_values.keys())
    exchange_rates = list(latest_rate_values.values())

    # Add the current date to all records
    rate_dates = [datetime.date.today()] * len(symbols)

    # Create a DataFrame
    latest_rates_df = pd.DataFrame({
        'symbol': symbols,
        'exchange_rate': exchange_rates,
        'rate_date': rate_dates
    })

    print("\nLatest Exchange Rates DataFrame:")
    print(latest_rates_df)

    return latest_rates_df

# Define function to retrieve historical exchange rate data
def fetch_historical_data(api_key, base_currency, start_date, end_date):
    """
    Fetches historical exchange rates from the Fixer.io API for a given date range.

    Parameters:
        api_key (str): API key for authentication.
        base_currency (str): Base currency for exchange rates.
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.

    Returns:
        pd.DataFrame: A DataFrame containing historical exchange rates.
    """
    url = 'http://data.fixer.io/api/timeseries'
    querystring = {
        "access_key": api_key,
        "start_date": start_date,
        "end_date": end_date,
        "base": base_currency
    }

    # Make the API call
    response = requests.get(url, params=querystring)
    response_json = response.json()

    # Check for successful API call
    if response_json.get('success', False):
        historical_rates = response_json.get('rates', {})
        historical_df = pd.DataFrame.from_dict(historical_rates, orient='index')
        historical_df.index.name = 'date'
        historical_df.reset_index(inplace=True)
        historical_df['base_currency'] = base_currency

        print("\nHistorical Exchange Rates DataFrame:")
        print(historical_df)

        return historical_df
    else:
        print("\nError: Failed to retrieve historical data.")
        print("Message:", response_json.get('error', {}).get('info', 'Unknown error'))
        return None

# Define function to calculate KPIs
def calculate_kpis(df):
    """
    Calculates key performance indicators (KPIs) such as max, min, and fluctuation for each currency.

    Parameters:
        df (pd.DataFrame): DataFrame containing historical exchange rates.

    Returns:
        pd.DataFrame: A summary DataFrame with max_rate, min_rate, and fluctuation for each currency.
    """
    rate_columns = df.columns.difference(['date', 'base_currency'])
    max_rates = df[rate_columns].max()
    min_rates = df[rate_columns].min()
    fluctuations = max_rates - min_rates

    kpi_summary = pd.DataFrame({
        'max_rate': max_rates,
        'min_rate': min_rates,
        'fluctuation': fluctuations
    })
    kpi_summary.index.name = 'currency'

    return kpi_summary

# Main section to execute the script
if __name__ == "__main__":
    # Fetch the latest exchange rates
    print("\nFetching latest exchange rates...")
    latest_rates_df = fetch_latest_rates(apikey)

    # Fetch historical exchange rate data
    print("\nFetching historical exchange rate data...")
    start_date = "2020-03-01"
    end_date = "2021-03-01"
    base_currency = "USD"
    historical_exchange_data = fetch_historical_data(apikey, base_currency, start_date, end_date)

    # Perform analysis if historical data is retrieved
    if historical_exchange_data is not None:
        print("\nBasic Statistics for Historical Data:")
        print(historical_exchange_data.describe())

        # Calculate KPIs
        kpi_summary = calculate_kpis(historical_exchange_data)
        print("\nKey Performance Indicators (KPIs):")
        print(kpi_summary)

        # Save KPIs to a CSV file
        kpi_summary.to_csv("kpi_summary.csv", index=True)
        print("\nKPI summary saved to 'kpi_summary.csv'.")
