
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
# For Base currency of USD return all output currencies from 01-01-2020 to 01-01-2021
querystring = {"base":"USD"}
#querystring = {"base":"USD","start_date":"2020-03-01","end_date":"2020-06-01"}
# Packages the requests, sends it, and catches the response all in one function
r = requests.get(url, params=querystring)
#r = requests.get(url, params=querystring)
# Then use the text attribute of r to read it as a string
response_json = r.json()
# Print response_json
print(response_json)

for key, value in response_json.items():
    print(key + ':', value)

#
import datetime
from datetime import datetime
latest_rate_values = (response_json['rates'])
#print(latest_rate_values)# Print data_values

#convert keys and values into individual lists
symbol = list(latest_rate_values.keys())
exchange_rate = list(latest_rate_values.values())
#print(symbol, exchange_rate)

rate_date = []
for key in latest_rate_values:
    rate_date.append(datetime.date.today())
    #print(close_datetime)  # Print close_datetime
print(rate_date) # Print type of time_time

import pandas as pd

latest_ex_rates_pd = pd.DataFrame({'symbol':[],'exchange_rate':[],'rate_date':[]}) # create an empty dataframe
# Make the column symbol equal to the list symbol
latest_ex_rates_pd['symbol'] = symbol
#print(mtbstock_pd)
# Make the column exchange_rate equal to the list exchange_rate
latest_ex_rates_pd['exchange_rate'] = exchange_rate
#print(mtbstock_pd)
# Make the column rate_date equal to the list rate_date
latest_ex_rates_pd['rate_date'] = rate_date
# print the DataFrame
print(latest_ex_rates_pd)
