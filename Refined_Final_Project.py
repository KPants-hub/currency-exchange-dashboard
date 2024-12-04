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
    url = 'http://data.fixer.io/api/latest'
    querystring = {"access_key": api_key, "base": "USD", "symbols": "EUR,JPY,GBP,AUD,CAD,DEM,INR,MXN,RUB,CNY"}

    # Make the API call
    response = requests.get(url, params=querystring)
    response_json = response.json()

    # Debugging: Print the full JSON response
    print("Full JSON Response:")
    print(response_json)

    # Extract exchange rates
    latest_rate_values = response_json.get('rates', {})
    latest_rate_date = response_json.get('date', {})
    if not latest_rate_values:
        print("\nError: No rates data found in the response.")
        return None
    # Extract latest exchange date
    rate_date = []
    for key in latest_rate_values:
        rate_date.append(latest_rate_date)
        if not latest_rate_date:
            print("\nError: No rates date found in the response.")
            return None

    # Convert the currency symbols and their exchange rates into lists
    symbols = list(latest_rate_values.keys())
    exchange_rates = list(latest_rate_values.values())

    # Create a DataFrame
    latest_rates_df = pd.DataFrame({
        'symbol': symbols,
        'exchange_rate': exchange_rates,
        'rate_date': rate_date
    })

    print("\nLatest Exchange Rates DataFrame:")
    print(latest_rates_df)

    # Save Latest Exchange Rates DataFrame save to latest_rates_df.csv
    latest_rates_df.to_csv('latest_rates_df.csv')
    print("\nLatest Exchange Rates DataFrame saved to 'latest_rates_df.csv'.")

    return latest_rates_df


# Define function to retrieve historical exchange rate data
def fetch_historical_data(api_key, base_currency, start_date, end_date, symbols):
    url = 'http://data.fixer.io/api/timeseries'
    querystring = {
        "access_key": api_key,
        "start_date": start_date,
        "end_date": end_date,
        "base": base_currency,  # Note: Free tier ignores the 'base' parameter.
        "symbols": symbols
    }

    try:
        # Make the API call
        response = requests.get(url, params=querystring)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        response_json = response.json()

        if not response_json.get('success', False):
            print("\nError: Failed to fetch historical data.")
            print("Message:", response_json.get('error', {}).get('info', 'Unknown error'))
            return None

        # Extract historical rates
        historical_rates = response_json.get('rates', {})

        # Transform data into the desired format
        data = []
        for date, rates in historical_rates.items():
            for currency, rate in rates.items():
                data.append({"date": date, "currency": currency, "rate": rate})

        # Create a DataFrame
        historical_df = pd.DataFrame(data)

        print("\nFormatted Historical Exchange Rates DataFrame:")
        print(historical_df)

        # Save DataFrame to CSV
        historical_df.to_csv('historic_ex_rate_df.csv', index=False)
        print("\nHistorical Exchange Rates DataFrame saved to 'historic_ex_rate_df.csv'.")

        return historical_df

    except requests.exceptions.RequestException as e:
        print("\nError: Could not fetch historical data.")
        print(e)
        return None


# Define function to retrieve historic trend exchange rate data
def fetch_historic_trend_data(api_key, base_currency, start_date, end_date, symbols):
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
        "base": base_currency,
        "symbols": symbols
    }

    # Make the API call
    response = requests.get(url, params=querystring)
    response_json = response.json()

    # Check for successful API call
    if response_json.get('success', False):
        historic_trend_rates = response_json.get('rates', {})
        historic_trend_df = pd.DataFrame.from_dict(historic_trend_rates, orient='index')
        historic_trend_df.index.name = 'date'
        historic_trend_df.reset_index(inplace=True)
        historic_trend_df['base_currency'] = base_currency

        print("\nHistoric Trend Exchange Rates DataFrame:")
        print(historic_trend_df)

        return historic_trend_df

    else:
        print("\nError: Failed to retrieve historic trend data.")
        print("Message:", response_json.get('error', {}).get('info', 'Unknown error'))
        return None
    


# Define function to calculate KPIs
def calculate_kpis(df):
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
    symbols = "EUR,JPY,GBP,AUD,CAD,DEM,INR,MXN,RUB,CNY"
    historical_exchange_data = fetch_historical_data(apikey, base_currency, start_date, end_date, symbols)

    # Perform analysis if historical data is retrieved
    if historical_exchange_data is not None:
        print("\nBasic Statistics for Historical Data:")
        print(historical_exchange_data)

        # Save Basic Stats Descr to historical_exchange_data.csv
        historical_exchange_data.to_csv("historical_exchange_data.csv", index=True)
        print("\nBasic Statistics for Historical Data save to 'historical_exchange_data'.")

        # Fetch historical exchange rate data
        print("\nFetching historical exchange rate data...")
        start_date = "2020-03-01"
        end_date = "2021-03-01"
        base_currency = "USD"
        symbols = "EUR,JPY,GBP,AUD,CAD,DEM,INR,MXN,RUB,CNY"
        historic_trend_data = fetch_historic_trend_data(apikey, base_currency, start_date, end_date, symbols)

        if historic_trend_data is not None:
            print("\nBasic Statistics for Historical Data:")
            print(historic_trend_data.describe())

            # Save Basic Stats Descr to historic_basic_stats.csv
            (historic_trend_data.describe()).to_csv("historic_trend_stats.csv", index=True)
            print("\nBasic Statistics for Historical Data save to 'historic_trend_stats.csv'.")

            # Calculate KPIs
            kpi_summary = calculate_kpis(historic_trend_data)
            print("\nKey Performance Indicators (KPIs):")
            print(kpi_summary)

            # Save KPIs to a CSV file
            kpi_summary.to_csv("kpi_summary.csv", index=True)
            print("\nKPI summary saved to 'kpi_summary.csv'.")
