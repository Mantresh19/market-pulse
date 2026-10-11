from fastapi import FastAPI
# Without this python code is just a local script and by using this we can use it as a app.get(req,res => {})
from fastapi.middleware.cors import CORSMiddleware
# if we don't use this then suppose if my front end is running on localhost 8080 and backend is running on local host 7080 then they wont connect with each other but after using this we can make them connect and share data with each other even if both are running on different localhosts
from fastapi.staticfiles import StaticFiles
# it lets the computer to serve the static files to the code such as css, js, html etc so you can just simply put the paths of the static files into your code stored into your computer and use them
import os

from fetch_data import download_stock_data
from detect_anomalies import find_market_anomalies
from fetch_news import get_stock_news
from plot_anomalies import create_anomaly_chart
from ai_analyst import score_headline_sentiment

app = FastAPI(title="MarketPulse AI API")
# this is used to listen a port

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    # 
    allow_methods = ["*"],
    # This allows all HTTP methods through the CORS policy such as (GET, POST, etc)
    allow_headers = ["*"],
    #
)
# This section is a CORS(Cross Origin Resource Sharing) feature

os.makedirs("data", exist_ok=True)
app.mount("/data", StaticFiles(directory="data"), name="data")

@app.get("/api/analyze/{ticker}")

def analyze_stock(ticker: str, z_threshold: float = 2.0):
    ticker = ticker.upper()

    download_stock_data(ticker=ticker, period="1y")
    anomalies_df = find_market_anomalies(ticker=ticker, z_threshold=z_threshold)
    chart_path = create_anomaly_chart(ticker=ticker, z_threshold=z_threshold)
    news_list = get_stock_news(ticker=ticker, limit=5)

    anomaly_events = []
    for date, row in anomalies_df.iterrows():
        anomaly_events.append({
            "date": str(date)[:10],
            "close": round(float(row["Close"]), 2),
            "daily_return_pct": round(float(row["Daily_Return"] * 100), 2),
            "z_score": round(float(row["Z_Score"]), 2)
        })
        
    total_score = 0
    for item in news_list:
        s_score = score_headline_sentiment(item["title"])
        item["sentiment_score"] = s_score
        total_score += s_score

    return{
        "ticker": ticker,
        "z_threshold": z_threshold,
        "total_anomalies": len(anomaly_events),
        "net_sentiment_score": total_score,
        "chart_url": f"http://localhost:8000/{chart_path}",
        "anomalies": anomaly_events,
        "news": news_list
    }