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
    df['Z_Score'] = (df['Daily_Return'] - df['Mean_Return_20d']) / df['Std_Return_20d']
    # This is the standard formula Z = X - x̄ = σ

    anomalies = df[df['Z_Score'].abs() > z_threshold]
    # abs() is a short of absolute value it strips off +,- signs eg. +2.3 will be 2.3

    print(f"\n Found {len(anomalies)} Market Anomalies for {ticker} (Threshold: {z_threshold} standard deviations):")

    summary = anomalies[['Close', 'Daily_Return', 'Z_Score']]
    # Here I put 2[[]], It just tells the computer to remove all the clutter and only show this special values eg. close,daily_return etc
    for date, row in summary.iterrows():
    # iterrows() is a pandas method which helps to loop through the data frame
    # date: the index for that specific day
    # row: a package containing that days data eg, close, daily_return, z-score
        date_str = str(date)[:10]
        # str(date): there is so much mess in pandas data like 2024.03.12 00.00.00... it just turns into pure text
        # [:10] grabs only first 10 characters eg. 2026.03.28 and ignore 00.00.00...
        pct = row['Daily_Return'] * 100
        # Converts that raw decimal back to human percentage
        z = row['Z_Score']
        # here we just saving Z_score which is inside of row value into Z
        direction = "🟢 SURGE" if pct > 0 else "🔴 DROP"
        print(f"[{date_str}] {direction}: {pct:+.2f}% (Z-Score: {z:+.2f}) | Close: ${row['Close']:+.2f}")
        
        return anomalies

if __name__ == "__main__":
    find_market_anomalies()