
# API directions from website
# #import requests
#url = "https://data.fixer.io/api/timeseries?access_key={PASTE_YOUR_API_KEY_HERE}"
#querystring = {"symbols":"USD,EUR","start_date":"2012-05-01","end_date"="2012-05-25"}
##response = requests.get(url, params=querystring)
#Parameter	Description
#access_key	[required] Your API Key.
#start_date	[required] The start date of your preferred timeframe.
#end_date	[required] The end date of your preferred timeframe.
#base	[optional] Enter the three-letter currency code of your preferred base currency.
#symbols	[optional] Enter a list of comma-separated currency codes to limit output currencies.

#First get most recent exchange rates relative to USD
import requests
# For this project, access the API and pull data.
apikey = '7bf403592be68c3af0287ed3ab4a19ac'
# url to return records for exchange rates
url = 'http://data.fixer.io/api/latest?access_key=7bf403592be68c3af0287ed3ab4a19ac'
# Identify parameters for the data we want to return
# For Base currency of USD return the latest conversion rate for the following :
# Europe, Japan, Great Britian, Australia, Canada, Germany, India, Mexico, Russia, China
querystring = {"base":"USD", "symbols":"EUR,JPY,GBP,AUD,CAD,DEM,INR,MXN,RUB,CNY"}
# Packages the requests, sends it, and catches the response all in one function
r = requests.get(url, params=querystring)
#r = requests.get(url, params=querystring)
# Then use the text attribute of r to read it as a string
response_json = r.json()
# Print response_json
print(response_json)

# convert keys
for key, value in response_json.items():
    print(key + ':', value)


# create dict for rates
latest_rate_values = (response_json['rates'])
# print the data associated with the rate
print(type(latest_rate_values))
latest_rate_date = (response_json['date'])
# print the date associated with the rate
print(latest_rate_date)

# create list of rate keys
symbol = list(latest_rate_values.keys())
# create list of rate values
exchange_rate = list(latest_rate_values.values())
print(symbol, exchange_rate)

import datetime
#create empty list to append rate date
rate_date = []
# loop through the rate data to append the date for each record
for key in latest_rate_values:
    rate_date.append(latest_rate_date)
print(rate_date) # Print type of time_time

import pandas as pd

# create an empty dataframe
latest_ex_rates_pd = pd.DataFrame({'symbol':[],'exchange_rate':[],'rate_date':[]})
# Make the column symbol equal to the list symbol
latest_ex_rates_pd['symbol'] = symbol

# Make the column exchange_rate equal to the list exchange_rate
latest_ex_rates_pd['exchange_rate'] = exchange_rate

# Make the column rate_date equal to the list close_datetime
latest_ex_rates_pd['rate_date'] = rate_date
# print the DataFrame
print(latest_ex_rates_pd)



#Get historic exchange rates relative to USD
import requests
# For this project, access the API and pull data.
apikey = '7bf403592be68c3af0287ed3ab4a19ac'
# url to return records for exchange rates
url = 'https://data.fixer.io/api/timeseries?access_key=7bf403592be68c3af0287ed3ab4a19ac'
# Identify parameters for the data we want to return
# For Base currency of USD return the historic conversion rate from 2020-01-01 to 2021-01-01 for the following :
# Europe, Japan, Great Britian, Australia, Canada, Germany, India, Mexico, Russia, China
querystring = {"base":"USD", "symbols":"EUR,JPY,GBP,AUD,CAD,DEM,INR,MXN,RUB,CNY", "start_date":"2020-01-01","end_date":"2021-01-01"}
# Packages the requests, sends it, and catches the response all in one function
r = requests.get(url, params=querystring)
# Then use the text attribute of r to read it as a string
response_json = r.json()
# Print response_json
print(response_json)

historic_dates = []
historic_rate_data = [[]]
for key in response_json['rates'].items():
    historic_dates.append(key)
    historic_rate_data.append(value)
print(historic_dates)
print(historic_rate_data)
print(type(historic_rate_data))

historic_rate_sym = list(historic_rate_data[0].keys())
print(historic_rate_sym)

need to get the value for each symbol?????

# create an empty dataframe
historic_ex_rates_pd = pd.DataFrame({'historic_symbol':[],'historic_exchange_rate':[],'historic_dates':[]})
# Make the column symbol equal to the list symbol
historic_ex_rates_pd['historic_symbol'] = symbol

# Make the column exchange_rate equal to the list exchange_rate
historic_ex_rates_pd['historic_exchange_rate'] = exchange_rate

# Make the column rate_date equal to the list close_datetime
historic_ex_rates_pd['historic_dates'] = historic_dates
# print the DataFrame
print(historic_ex_rates_pd)

