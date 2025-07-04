import yfinance as yf
import pandas as pd

# Function to get OHLC data using yfinance
def OHLCHistory(symbol, interval, fdate, todate):
    try:
        # Fetch the historical data from Yahoo Finance
        data = yf.download(tickers=symbol, start=fdate, end=todate, interval=interval)
        data = data.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })
        return data
    except Exception as e:
        print("API call failed:", e)
        return None

# Example usage of the OHLCHistory function
symbol = 'RELIANCE.NS'  # example symbol (ensure it matches Yahoo Finance ticker format)
interval = '1d'  # interval could be '1m', '2m', '5m', '15m', '1d', '1wk', etc.
fdate = '2023-01-01'  # from date
todate = '2023-07-01'  # to date

# Get historical data
historical_data = OHLCHistory(symbol, interval, fdate, todate)
if historical_data is not None:
    print(historical_data)
__________________________________________________________________________________________________________________________________________________________________________________________________
import yfinance as yf
import pandas as pd

# Function to get option chain data for a specific strike price
def get_option_chain(symbol, expiry, strike_price):
    try:
        # Fetch the Ticker object
        ticker = yf.Ticker(symbol)

        # Fetch options expiration dates
        expirations = ticker.options
        if expiry not in expirations:
            print(f"Expiry date {expiry} not found in available expirations: {expirations}")
            return None, None

        # Fetch the option chain for the given expiration date
        opt_chain = ticker.option_chain(expiry)
        calls = opt_chain.calls
        puts = opt_chain.puts

        # Filter the calls and puts by the specific strike price
        filtered_calls = calls[calls['strike'] == strike_price].reset_index(drop=True)
        filtered_puts = puts[puts['strike'] == strike_price].reset_index(drop=True)

        return filtered_calls, filtered_puts
    except Exception as e:
        print("API call failed:", e)
        return None, None

# Example usage of the get_option_chain function
symbol = 'ADANIENT.NS'  # example symbol
expiry = '2025-07-31'  # example expiry date (YYYY-MM-DD)
strike_price = 2600  # example strike price

# Get the option chain data
calls, puts = get_option_chain(symbol, expiry, strike_price)
if calls is not None and puts is not None:
    print("Calls at strike price", strike_price)
    print(calls.to_string(index=False))
    print("\nPuts at strike price", strike_price)
    print(puts.to_string(index=False))
