import yfinance as yf
import time
from datetime import datetime, timedelta

# List of NSE shares and their Yahoo Finance tickers
# Note: Ensure these tickers are accurate. You can verify on Yahoo Finance.
NSE_STOCKS = {
    "HDFC Bank Ltd.": "HDFCBANK.NS",
    "ICICI Bank Ltd.": "ICICIBANK.NS",
    "Reliance Industries Ltd.": "RELIANCE.NS",
    "Infosys Ltd.": "INFY.NS",
    "Bharti Airtel Ltd.": "BHARTIARTL.NS",
    "Larsen & Toubro Ltd.": "LT.NS",
    "ITC Ltd.": "ITC.NS",
    "Tata Consultancy Services Ltd.": "TCS.NS",
    "Axis Bank Ltd.": "AXISBANK.NS",
    "State Bank of India": "SBIN.NS",
}

# --- Configuration ---
INITIAL_DROP_PERCENTAGE = 20
SUBSEQUENT_DROP_PERCENTAGE = 1
CHECK_INTERVAL_SECONDS = 60  # Check every 1 minute for alerts
SUMMARY_INTERVAL_SECONDS = 300 # Print summary every 5 minutes

# Dictionary to store monitoring status for each stock
# { 'TICKER': {'52_week_high': None, 'current_price': None, 'initial_drop_price': None, 'last_notified_price': None, 'initial_drop_alerted': False} }
monitoring_status = {}
last_summary_report_time = datetime.now()

def get_stock_data(ticker_symbol):
    """Fetches current price and 52-week high for a given ticker."""
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info

        current_price = info.get('currentPrice')
        fifty_two_week_high = info.get('fiftyTwoWeekHigh')

        if current_price is None or fifty_two_week_high is None:
            print(f"Warning: Could not retrieve current price or 52-week high for {ticker_symbol}. Skipping.")
            return None, None

        return current_price, fifty_two_week_high
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None, None

def check_and_notify(stock_name, ticker, current_price, fifty_two_week_high):
    """
    Checks for price drops and sends notifications.
    """
    global monitoring_status

    if ticker not in monitoring_status:
        # This block might not be strictly needed if initial collection handles it
        # but serves as a fallback or for dynamically added stocks.
        monitoring_status[ticker] = {
            '52_week_high': fifty_two_week_high,
            'current_price': current_price, # Store current price for summary
            'initial_drop_price': None,
            'last_notified_price': None,
            'initial_drop_alerted': False
        }
    else:
        # Update current price for subsequent checks and summary
        monitoring_status[ticker]['current_price'] = current_price

    status = monitoring_status[ticker]

    # Calculate initial 20% drop threshold
    initial_drop_threshold = fifty_two_week_high * (1 - INITIAL_DROP_PERCENTAGE / 100)

    # Check for initial 20% drop
    if not status['initial_drop_alerted'] and current_price <= initial_drop_threshold:
        print(f"\n--- ALERT! {stock_name} ({ticker}) ---")
        print(f"Current Price: ₹{current_price:.2f}")
        print(f"52-Week High: ₹{fifty_two_week_high:.2f}")
        print(f"Price is {INITIAL_DROP_PERCENTAGE:.0f}% down from its 52-week high (₹{initial_drop_threshold:.2f}).")
        status['initial_drop_alerted'] = True
        status['initial_drop_price'] = current_price
        status['last_notified_price'] = current_price
        print("Monitoring for further 1% drops...")
        return

    # If initial drop has been alerted, check for subsequent 1% drops
    if status['initial_drop_alerted'] and current_price < status['last_notified_price']:
        # Calculate the next 1% drop threshold from the initial drop price
        next_drop_threshold = status['last_notified_price'] * (1 - SUBSEQUENT_DROP_PERCENTAGE / 100)

        if current_price <= next_drop_threshold:
            percentage_fall_from_initial = ((status['initial_drop_price'] - current_price) / status['initial_drop_price']) * 100
            print(f"\n--- UPDATE! {stock_name} ({ticker}) ---")
            print(f"Current Price: ₹{current_price:.2f}")
            print(f"Price has fallen another {SUBSEQUENT_DROP_PERCENTAGE:.0f}% from ₹{status['last_notified_price']:.2f}.")
            print(f"Total fall from 20% down level: {percentage_fall_from_initial:.2f}%")
            status['last_notified_price'] = current_price
            return
    elif status['initial_drop_alerted'] and current_price > status['last_notified_price'] * (1 + SUBSEQUENT_DROP_PERCENTAGE / 100):
        # If the price has recovered significantly, reset the last notified price
        # This prevents repeated notifications for small fluctuations around the last notified price
        status['last_notified_price'] = current_price


def print_summary_status():
    """Prints the percentage difference from 52-week high for all monitored stocks."""
    print(f"\n--- Summary Report ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) ---")
    print(f"{'Stock Name':<30} | {'Current Price':>15} | {'52-Week High':>15} | {'% Down from High':>18}")
    print("-" * 85)
    for stock_name, ticker in NSE_STOCKS.items():
        if ticker in monitoring_status:
            status = monitoring_status[ticker]
            current_price = status.get('current_price')
            fifty_two_week_high = status.get('52_week_high')

            if current_price is not None and fifty_two_week_high is not None and fifty_two_week_high > 0:
                percentage_down = ((fifty_two_week_high - current_price) / fifty_two_week_high) * 100
                print(f"{stock_name:<30} | ₹{current_price:>13.2f} | ₹{fifty_two_week_high:>13.2f} | {percentage_down:>16.2f}%")
            else:
                print(f"{stock_name:<30} | {'Data N/A':>15} | {'Data N/A':>15} | {'Data N/A':>18}")
        else:
            print(f"{stock_name:<30} | {'Not Monitored Yet':<60}")
    print("-" * 85)

def main():
    global last_summary_report_time
    print("Starting stock price tracker for NSE shares...")
    print("Initial 52-week high data collection in progress...")

    # Initial data collection to populate 52-week highs and current prices
    for stock_name, ticker in NSE_STOCKS.items():
        current_price, high_52_week = get_stock_data(ticker)
        if current_price is not None and high_52_week is not None:
            monitoring_status[ticker] = {
                '52_week_high': high_52_week,
                'current_price': current_price, # Store current price here
                'initial_drop_price': None,
                'last_notified_price': None,
                'initial_drop_alerted': False
            }
            print(f"Initialized {stock_name} ({ticker}): 52-Week High = ₹{high_52_week:.2f}, Current Price = ₹{current_price:.2f}")
            # Check for initial drop immediately after fetching 52-week high
            # In case the stock is already below 20% of its 52-week high at startup
            check_and_notify(stock_name, ticker, current_price, high_52_week)
        time.sleep(1) # Be mindful of API rate limits

    print(f"\nMonitoring started. Checking every {CHECK_INTERVAL_SECONDS} seconds for alerts.")
    print(f"Summary report will be printed every {SUMMARY_INTERVAL_SECONDS / 60:.0f} minutes.")

    while True:
        current_loop_start_time = datetime.now()
        for stock_name, ticker in NSE_STOCKS.items():
            current_price, _ = get_stock_data(ticker) # We only need current price for ongoing checks, 52-week high is in monitoring_status
            if current_price is not None and ticker in monitoring_status:
                # Update current price in monitoring status before checking and notifying
                monitoring_status[ticker]['current_price'] = current_price
                check_and_notify(stock_name, ticker, current_price, monitoring_status[ticker]['52_week_high'])
            time.sleep(1) # Small delay between checking each stock to avoid hitting rate limits

        # Check if it's time for the summary report
        if datetime.now() - last_summary_report_time >= timedelta(seconds=SUMMARY_INTERVAL_SECONDS):
            print_summary_status()
            last_summary_report_time = datetime.now() # Reset timer for the next summary

        print(f"\n--- Completed 1-minute check cycle at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        # Ensure the loop waits for the remaining time to complete the CHECK_INTERVAL_SECONDS
        time_elapsed = (datetime.now() - current_loop_start_time).total_seconds()
        sleep_time = CHECK_INTERVAL_SECONDS - time_elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

if __name__ == "__main__":
    main()
