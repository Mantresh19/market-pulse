import pandas as pd
import matplotlib.pyplot as plt
from detect_anomalies import find_market_anomalies

def create_anomaly_chart(ticker="AAPL", z_threshold = 2.0):
    #1. Load the full 1-year price history
    file_path = f"data/{ticker}_raw.csv"
    # f string we use so we can write functional code into the {functional} even if there is ""
    # data is the folder containing the ticker(aapl csv) and "/" means go inside this folder
    df = pd.read_csv(file_path, index_col=0)
    # df is dataframe and it is a variable which contains rows and columns in pandas
    df.index = pd.to_datetime(df.index, utc=True)
    # to_datetime turns dumb text into genuine calendar moments. Now matplotlib knows how many days or months passed between points eg when a csv loads then python treats the dates just like words eg("Banana") or ("Hello") If dates remain plain text, the plotting tool (matplotlib) doesn't know "2024-01-02" comes 1 day after "2024-01-01". It treats them like categorical words.
    # utc=True locks every timestamp to one single universal world clock so timestamps don't crash when compared across different datasets.

    # 2. Get the anomaly days from your detector
    anomalies = find_market_anomalies(ticker=ticker, z_threshold=z_threshold)
    anomalies.index = pd.to_datetime(anomalies.index, utc=True)
    # .index is just telling computer take the whole left side strip and convert every single one from plain text to real calendar time and slap them back onto the left side of the table
    # In pandas: The column headers across the top are accessed with df.columns. That strip of row labels running down the left side is accessed with df.index.
    
    # Spilit anomalies into surges (Z>0) and Drops (Z<0)
    surges = anomalies[anomalies['Z_Score'] > 0]
    drops = anomalies[anomalies['Z_Score'] < 0]
    # it just means go inside the anomalies table and in the same table compare z_score with 0

    # 3. Create the visual chart canvas (12 inches wide, 6 inches tall)
    plt.figure(figsize=(12,6))

    # Draw the continuous daily closing price line
    plt.plot(df.index, df['Close'], label=f"{ticker} Closing Price", color="#2563eb", linewidth=1.8)
    # There is a rule in matplotlib that first give me x-axis then y-axis this 2 are x&y axis df.index, df['Close']

    # Draw Red Dots on Surge Anomalies
    plt.scatter(surges.index, surges['Close'], color="#10b981", label="Surge Anomaly(Z > +2)", s=80, zorder=5)
    # in matplotlib there are 2 things 1) plt.plot it just connects the dots with the lines 2) plt.scatter keeps the dots individual and keep them in the air and don't connect them
    # s=80 is the size of the green/red dot, and because of z_order it's not letting the dots hide underneath the graph

    # Draw Red Dots on Drop Anomalies
    plt.scatter(drops.index, drops["Close"], color="#ef4444", label="Drop Anomaly (Z < -2)", s=80, zorder=5)

    # Add chart title, axis, labels & grid
    plt.title(f"{ticker} - 1-Year Price & Statistical Volatility Anomalies", fontsize=14, fontweight="bold")
    # plt.title is used to print date right in the top center of the graph
    plt.xlabel("Date")
    # this line is used to print date right in the center of the x axis
    plt.ylabel("Stock Price ($ USD)")
    # Same as x axis but this is y
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Save the high resolution image into the data folder
    chart_path = f"data/{ticker}_chart.png"
    plt.tight_layout()
    # 1. What problem does it solve? => Large titles and axis labels can sometimes get cut off or touch the edges of the chart.
    # 2. What does this line do? => It automatically adjusts the chart spacing so that the title, labels, and numbers fit neatly inside without being cropped.
    plt.savefig(chart_path, dpi=150)
    #What does it do? => Saves the chart as a PNG image file instead of only displaying it `chart_path`: Specifies where and under what name the file is saved, e.g. `"charts/AAPL_anomalies.png"`.
    # `dpi=150`:Controls image quality. 150 DPI makes the image sharper and clearer without making the file unnecessarily large.
    plt.close()