import yfinance as yf

def get_adj_close(ticker, start_date, end_date):
    # Define the ticker symbol and date range
    ticker_symbol = ticker
    start_date = start_date
    end_date = end_date

    # Fetch historical data from Yahoo Finance
    data = yf.download(ticker_symbol, start=start_date, end=end_date, actions=True)

    # Filter for adjusted closing prices
    adj_close_data = data['Adj Close'].to_frame()

    # Rename the column for clarity
    adj_close_data.rename(columns={'Adj Close': 'Adjusted Close'}, inplace=True)

    # Print the first few rows of the DataFrame
    print(adj_close_data.head())

    return adj_close_data