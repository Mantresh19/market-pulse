# The goal of ai analyst is to combine everything altogether
# 1st step import the codes we wrote earlier
from detect_anomalies import find_market_anomalies
from fetch_news import get_stock_news

# It's like keywords matching algorithm like you made your uni project using this algo
BULLISH_WORDS = ["rises", "record", "high", "buy", "favourite", "surge", "beat", "growth", "strong"]
BEARISH_WORDS = ["threaten", "softer", "drop", "fall", "miss", "risk", "lawsuit", "weak", "done"]

def score_headline_sentiment(headline):
    # Here we lowercase the headline suppose if in the yahoo finance DB there is news headline but it starts with 'U'ppercase then the keywords matching algorithm we're using is useless because "Headline" and "headline are two different words"
    text = headline.lower()
    # Start score from 0
    score = 0

    for word in BULLISH_WORDS:
        if word in text:
            score += 1

    for word in BEARISH_WORDS:
        if word in text:
            score -= 1

    return score

def generate_intelligence_report(ticker="AAPL"):
    # Just a print statement mate nothing complex
    print(f"\n🧠 INITALIZING AI MARKET ANALYST FOR {ticker}...")
    print("=" * 60)

    # Call your anomaly detector
    anomalies = find_market_anomalies(ticker=ticker, z_threshold=2.0)

    # Call fetch news
    news_list = get_stock_news(ticker=ticker, limit=5)

    