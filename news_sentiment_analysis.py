import yfinance as yf
from textblob import TextBlob
import requests
from bs4 import BeautifulSoup

def get_news(ticker):
    try:
        url = f"https://finance.yahoo.com/quote/{ticker}/news?p={ticker}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, "html.parser")
        news_list = []

        # Adapt the CSS selectors based on the actual Yahoo Finance page structure
        for news_item in soup.select(".Mb(5px)"): # Example selector, adjust as needed
            title_element = news_item.select_one("a") # Example selector, adjust as needed
            if title_element:
              title = title_element.text.strip()
              link = title_element["href"]
              news_list.append({"headline": title, "link": link})

        return news_list

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# Step 1: Get stock data from Yahoo Finance
def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    stock_data = stock.history(period='5d')  # Last 5 days of data
    return stock_data

# Step 2: Get news for the company from Yahoo Finance
def get_news(ticker):
    stock = yf.Ticker(ticker)
    news = stock.news  # Get the latest news related to the ticker
    print(news)  # Print the news data to inspect its structure
    return news

# Step 3: Analyze sentiment of news headlines
def analyze_sentiment(news_headlines):
    sentiment = {'Positive': 0, 'Neutral': 0, 'Negative': 0}

    for article in news_headlines:
        headline = article.get('headline', '')  # Use 'headline' or correct key if 'title' doesn't exist
        analysis = TextBlob(headline)
        polarity = analysis.sentiment.polarity

        if polarity > 0:
            sentiment['Positive'] += 1
        elif polarity == 0:
            sentiment['Neutral'] += 1
        else:
            sentiment['Negative'] += 1

    return sentiment

# Step 4: Combine sentiment analysis with stock data to generate a news indicator
def news_indicator(stock_data, sentiment, news):
    if not news:
        print("No news headlines were fetched.")
        return

    close_price = stock_data['Close'].iloc[-1]  # Last closing price
    sentiment_score = (sentiment['Positive'] - sentiment['Negative']) / len(news) * 100  # Basic sentiment score

    print("\nNews Indicator:")
    print(f"Last Closing Price: {close_price}")
    print(f"Sentiment Score (Positive vs Negative): {sentiment_score}%")

    # Simple logic: if positive sentiment > 50%, buy; else if negative sentiment > 50%, sell
    if sentiment_score > 50:
        print("Indicator: Buy")
    elif sentiment_score < -50:
        print("Indicator: Sell")
    else:
        print("Indicator: Hold")

# Main: Get user input for company name or ticker symbol
query = input("Enter the company name or ticker symbol for which you want news: ")

# Try to fetch the news and stock data for the entered query
news = get_news(query)

# If the query is valid, get stock data
if news:
    print(f"\nFetching news for: {query}")

    # Get stock data for the entered ticker
    stock_data = get_stock_data(query)  # Stock data for the company

    sentiment = analyze_sentiment(news)
    news_indicator(stock_data, sentiment, news)
else:
    print("No news data found for the entered ticker symbol.")
