import requests
import random

# Your Alpha Vantage API key
API_KEY = "TKTW303LZCG3PS3R"

def fetch_stock_market_value(symbol):
    """
    Fetch the current closing price for the given stock symbol using the
    Alpha Vantage TIME_SERIES_DAILY endpoint.
    
    Parameters:
        symbol (str): The stock symbol (e.g., "IBM" or "AAPL").
        
    Returns:
        float: The latest closing price.
        
    Raises:
        ValueError: If the data for the symbol cannot be retrieved.
    """
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": API_KEY,
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    try:
        # Retrieve the daily time series data
        time_series = data["Time Series (Daily)"]
        # Get the most recent date available
        latest_date = sorted(time_series.keys(), reverse=True)[0]
        latest_data = time_series[latest_date]
        # Use the closing price as the stock value
        return float(latest_data["4. close"])
    except KeyError:
        raise ValueError(f"Could not retrieve data for symbol {symbol}. Response: {data}")

def fetch_today_transaction_count():
    """
    Simulates fetching the number of transactions created today.
    In a real-world scenario, this might come from a blockchain or transaction
    tracking API. Here we simply simulate it with a random number.
    
    Returns:
        int: Simulated transaction count.
    """
    return random.randint(10, 100)

def calculate_airchip_token_value():
    """
    Calculates the AirChip token value based on:
      - The current value of 'eggs' (IBM's stock price).
      - The current value of 'chickens' (AAPL's stock price).
      - The number of transactions created today (simulated).
    
    The formula is:
          token_value = ((egg_value / chicken_value) * 7) / transaction_count
          
    Returns:
        float: Calculated AirChip token value.
    """
    # For demonstration, we use IBM as the "egg" and AAPL as the "chicken".
    egg_value = fetch_stock_market_value("IBM")
    chicken_value = fetch_stock_market_value("AAPL")
    transaction_count = fetch_today_transaction_count()
    
    if transaction_count == 0:
        raise ValueError("Transaction count must be greater than 0.")
    
    token_value = ((egg_value / chicken_value) * 7) / transaction_count
    
    # Print the fetched values for clarity
    print(f"IBM (Egg) closing price: {egg_value:.2f}")
    print(f"AAPL (Chicken) closing price: {chicken_value:.2f}")
    print(f"Simulated transaction count: {transaction_count}")
    
    return token_value

if __name__ == "__main__":
    try:
        token_value = calculate_airchip_token_value()
        print(f"\nThe calculated AirChip token value is: {token_value:.4f}")
    except Exception as e:
        print("Error calculating token value:", e)
