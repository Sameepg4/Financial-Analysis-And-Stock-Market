import requests
import pandas as pd
sesi=requests.Session()
headers={}
headers['user-agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'

a=sesi.get("https://www.nseindia.com/", headers=headers)

indices = ['BANKNIFTY', 'FINNIFTY', 'NIFTY']


def FetchOptionChainfromNSE (scrip):
    if scrip in indices:
        url=f"https://www.nseindia.com/api/option-chain-indices?symbol={scrip}"
    else:
        symbol4NSE = scrip.replace('&', '%26')
        url=f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol4NSE}"
    a=sesi.get(url, headers=headers)
    return a.json()['records']

option_chain_record = FetchOptionChainfromNSE ("TCS")

______________________________________________________________________________________________________________________________________________________________________________________________________________________
indices = ['BANKNIFTY', 'FINNIFTY', 'NIFTY']
def FetchOptionChainfromNSE (scrip):
  if scrip in indices:
    url=f"https://www.nseindia.com/api/option-chain-indices?symbol={scrip}"
  else:
    symbol4NSE = scrip.replace('&', '%26')
    url=f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol4NSE}"
  a=sesi.get(url, headers=headers)
  return a.json() ['records']
option_chain_record = FetchOptionChainfromNSE ("ITC")
option_chain_record
____________________________________________________________________________________________________________________________________________________________________________________________________________________

ExpiryDate = '31-JUL-2025'
# Now you can filter the DataFrame
# Define option_chain_data_df by assigning it to the return value of pd.DataFrame()
option_chain_data_df = pd.DataFrame(option_chain_record)
option_chain_data_df = option_chain_data_df[(option_chain_data_df.expiryDate == ExpiryDate)]
_____________________________________________________________________________________________________________________________________________________________________________________________________________________
option_chain = pd.DataFrame()
option_chain
option_chain ['strikePrice'] = option_chain_data_df ['strikePrice']
option_chain ['expiry Date'] = option_chain_data_df ['expiryDate']
option_chain
_____________________________________________________________________________________________________________________________________________________________________________________________________________________

ExpiryDate = '29-Sep-2022'
option_chain_data_df = option_chain_data_df[(option_chain_data_df.expiryDate == ExpiryDate)]
option_chain_data_df
____________________________________________________________________________________________________________________________________________________________________________________________________________________
OptionChain_CE = pd.DataFrame()
OptionChain_CE['CE'] = option_chain_data_df ['CE']
OptionChain_CE   
____________________________________________________________________________________________________________________________________________________________________________________________________________
OptionChain_PE_expand= pd.concat([Optioncmain_PE.drop(['PE'], axis=1), OptionChain_PE['PE'].apply(pd.Series)], axis=1)
OptionChain_CE_expand= pd.concat([OptionChain_CE.drop(['CE'], axis=1), OptionChain_CE['CE'].apply(pd.Series)), axis=1)
____________________________________________________________________________________________________________________________________________________________________________________________________________
goo!pip install pandas # Install pandas library
!pip install requests # Install requests library

import requests
import pandas as pd

sesi=requests.Session()
headers={}
headers['user-agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'

a=sesi.get("https://www.nseindia.com/", headers=headers)

indices = ['BANKNIFTY', 'FINNIFTY', 'NIFTY']


def FetchOptionChainfromNSE (scrip):
    if scrip in indices:
        url=f"https://www.nseindia.com/api/option-chain-indices?symbol={scrip}"
    else:
        symbol4NSE = scrip.replace('&', '%26')
        url=f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol4NSE}"
    a=sesi.get(url, headers=headers)
    return a.json()['records']

option_chain_record = FetchOptionChainfromNSE ("ITC") # Fetch data for ITC

ExpiryDate = '29-Sep-2022' # Define expiry date
# Now you can filter the DataFrame
# Define option_chain_data_df by assigning it to the return value of pd.DataFrame()
option_chain_data_df = pd.DataFrame(option_chain_record)
option_chain_data_df = option_chain_data_df[(option_chain_data_df.expiryDate == ExpiryDate)] # Filter dataframe

option_chain = pd.DataFrame() # Create an empty dataframe
option_chain
option_chain ['strikePrice'] = option_chain_data_df ['strikePrice'] # Assign strikePrice column
option_chain ['expiry Date'] = option_chain_data_df ['expiryDate'] # Assign expiryDate column
option_chain
_______________________________________________________________________________________________________________________________________________________________________________________________________
