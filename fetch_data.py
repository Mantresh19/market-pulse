import yfinance as yf
import os

def download_stock_data(ticker = "AAPL", period="1y"):
    print(f" Fetching live data for {ticker} from yahoo finance")

    stock = yf.Ticker(ticker)
    df = stock.history(period=period);

    os.makedirs("data", exist_ok=True)

    file_path = f"data/{ticker}_raw.csv"
    df.to_csv(file_path)
    print(f" Saved {len(df)} days of data to {file_path}")

    print("\n Here is a preview of the data:")
    print(df.head())

    return df
if __name__ == "__main__":
    download_stock_data()

