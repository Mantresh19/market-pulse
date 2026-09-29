import pandas as pd
import numpy as np

def find_market_anomalies(ticker="AAPL", z_threshold=2.0):
    file_path = f"data/{ticker}_raw.csv"

    df = pd.read_csv(file_path, index_col=0, parse_dates=True)

    df['Daily_Return'] = df['Close'].pct_change()
    # Here Close is the closing price of the market everyday
    # pct is shortform of % & is a built in function is doing a mathematical calculation
    # it calculates todays close - yesterdays close / yesterdays close 
    # eg yesterdays closing price was 10£ and todays 11£ it went up by 1£ soo 1/10 = 0.10% = 10% inc
    # change is comparing todays prices with yesterdays
    # The dot '.' here is telling the computer to take closest prices do this action
    # () is used to run that function

    df['Mean_Return_20d'] = df['Daily_Return'].rolling(window=20).mean()
    # rolling window = 20 is pulling up recent last 20 days data that's it
    # .mean() is calculating average

    df['Std_Return_20d'] = df['Daily_Return'].rolling(window=20).std()
    # std is shortform of standard deviation

    # The Z-Score formula 
    df['Z_Score'] = (df['Daily_Return'] - df['Mean_Return_20d'] / df['Std_Return_20d'])
    # This is the standard formula Z = X - x̄ = σ

    anomalies = df[df['Z_Score'].abs() > z_threshold]
    # abs() is a short of absolute value it strips off +,- signs eg. +2.3 will be 2.3

    print(f"\n Found {len(anomalies)} Market Anomalies for {ticker} (Threshold: {z_threshold} standard deviations):")

    summary = anomalies[['Close', 'Daily_Return', 'Z_Score']]
    # Here I put 2[[]], It just tells the computer to remove all the clutter and only show this special values eg. close,daily_return etc
    for date, row in summary.iterrows():
        date_str = str(date)[:10]
        pct = row