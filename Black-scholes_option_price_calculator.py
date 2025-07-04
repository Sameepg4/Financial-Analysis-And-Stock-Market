# Run the calculator when the script is executed
# prompt: make adjustments in the above code and the let the user enter the historical volatility instead of fetching the information from the yahoo finance database

import yfinance as yf
import numpy as np
from scipy.stats import norm
import datetime

# --- Black-Scholes Model Implementation ---
def black_scholes(S, K, T, r, sigma, option_type, q=0):
    """
    Calculates the theoretical price of a European option using the Black-Scholes model.

    Parameters:
    S (float): Current price of the underlying asset
    K (float): Strike price of the option
    T (float): Time to expiration (in years)
    r (float): Risk-free interest rate (annualized)
    sigma (float): Volatility of the underlying asset (annualized)
    option_type (str): Type of option ('call' or 'put')
    q (float): Dividend yield (annualized, default is 0)

    Returns:
    float: The theoretical price of the option.
    """
    if T <= 0:
        return max(0, S - K) if option_type == 'call' else max(0, K - S) # Option expires today

    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return price

# --- Data Fetching Function ---
def get_stock_data(ticker_symbol):
    """
    Fetches live stock data for a given ticker symbol.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)
        info = ticker.info
        current_price = info.get('currentPrice')
        dividend_yield = info.get('dividendYield', 0) # Default to 0 if not found
        return current_price, dividend_yield
    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")
        return None, None

def days_to_years(expiration_date_str):
    """
    Converts a date string to time to expiration in years.
    Date string format: YYYY-MM-DD
    """
    try:
        expiration_date = datetime.datetime.strptime(expiration_date_str, '%Y-%m-%d').date()
        today = datetime.date.today()

        if expiration_date < today:
            print("Expiration date is in the past.")
            return 0.0

        time_to_maturity_days = (expiration_date - today).days
        time_to_maturity_years = time_to_maturity_days / 365.0
        return time_to_maturity_years
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return None

# --- Main Calculator Logic ---
def run_black_scholes_calculator():
    print("--- Black-Scholes Option Price Calculator ---")

    while True:
        ticker_symbol = input("Enter stock ticker symbol (e.g., AAPL): ").strip().upper()
        if not ticker_symbol:
            print("Ticker symbol cannot be empty.")
            continue
        break

    current_price, dividend_yield = get_stock_data(ticker_symbol)
    if current_price is None:
        print("Could not retrieve current stock price. Please check the ticker symbol or internet connection.")
        return

    print(f"Current stock price for {ticker_symbol}: ${current_price:.2f}")
    print(f"Estimated dividend yield: {dividend_yield*100:.2f}%")

    # Get Strike Price
    while True:
        try:
            strike_price = float(input("Enter option strike price: "))
            if strike_price <= 0:
                print("Strike price must be positive.")
                continue
            break
        except ValueError:
            print("Invalid strike price. Please enter a number.")

    # Get Expiration Date
    while True:
        expiration_date_str = input("Enter option expiration date (YYYY-MM-DD): ").strip()
        time_to_expiration_years = days_to_years(expiration_date_str)
        if time_to_expiration_years is not None:
            if time_to_expiration_years == 0 and datetime.datetime.strptime(expiration_date_str, '%Y-%m-%d').date() < datetime.date.today():
                print("Expiration date is in the past. Options expired.")
                return
            break

    # Get Risk-Free Rate
    while True:
        try:
            risk_free_rate_str = input("Enter risk-free interest rate (e.g., 0.02 for 2%, default 0.02): ").strip()
            risk_free_rate = float(risk_free_rate_str) if risk_free_rate_str else 0.02
            if not (0 <= risk_free_rate <= 1): # Ensure it's a reasonable percentage
                print("Risk-free rate should be between 0 and 1 (e.g., 0.02).")
                continue
            break
        except ValueError:
            print("Invalid risk-free rate. Please enter a number.")

    # Get Volatility from User
    while True:
        try:
            volatility_str = input("Enter volatility (e.g., 0.20 for 20%): ").strip()
            volatility = float(volatility_str)
            if volatility <= 0:
                 print("Volatility must be positive.")
                 continue
            break
        except ValueError:
            print("Invalid volatility. Please enter a number.")

    print("\n--- Results ---")
    # Calculate Call Option Price
    call_price = black_scholes(
        S=current_price,
        K=strike_price,
        T=time_to_expiration_years,
        r=risk_free_rate,
        sigma=volatility,
        option_type='call',
        q=dividend_yield
    )
    print(f"Call Option Price: ${call_price:.2f}")

    # Calculate Put Option Price
    put_price = black_scholes(
        S=current_price,
        K=strike_price,
        T=time_to_expiration_years,
        r=risk_free_rate,
        sigma=volatility,
        option_type='put',
        q=dividend_yield
    )
    print(f"Put Option Price: ${put_price:.2f}")

# Run the calculator when the script is executed
if __name__ == "__main__":
    run_black_scholes_calculator()
