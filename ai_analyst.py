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

    print("\n📊 RUNNING FINANCIAL NLP SENTIMENT ANALYSIS:")
    total_score = 0
    for item in news_list:
    # Go to every news article and access it
        title = item["title"]
        s_score = score_headline_sentiment(title)
        total_score += s_score

        if total_score > 0:
            tag = "🟢 BULLISH"
        elif s_score < 0:
            tag = "🔴 BEARISH"
        else:
            tag = "⚪️ NEUTRAL"

        print(f" {tag} (Score: {s_score:+d}) -> {title}")

    worst_day = anomalies.loc[anomalies['Z_Score'].abs().idxmax()]
    # anomalies.loc here ".loc" is a pandas tool which scrapes date from idxmax containing(open, close, volume. etc....)
    # [anomalies[Z_Score]] is just anomalies grabbing the column named Z_Score from anomalies DF
    # abs is absolute value converting any negative numbers into positive eg -4.2 becomes 4.2 and why we do that? is because if there is a crash which is more than our threshold if it's -4 or something then our computer will think that it's less than our threshold but it's still a crash the only goal here to detect a crash
    # idx max just finds a highest value in that absolute field and returns it's row index label etc
    worst_date = str(worst_day.name)[:10]
    # here .name contains the column name etc.. and :10 is give me upto 10 rows only
    worst_return = worst_day['Daily_Return'] * 100
    # suppose if worst day gives you -4.200 then it will convert it into *100 which will be 4.2 
    worst_z = worst_day['Z_Score']

    if total_score > 0:
        overall_mood = "BULLISH (Positive Momentum)"
    elif total_score < 0:
        overall_mood = "BEARISH (Risk / Caution)"
    else:
        overall_mood = "NEUTRAL (Mixed Signals)"

    # here we print final executive briefing
    print("\n" + "=" * 60)
    print(f"EXECUTIVE AI BRIEFING: {ticker}")
    print("=" * 60)
    print(f". 1-Year Volatility Events: {len(anomalies)} statistical anomalies detected")
    print(f". Most Extreme Shock Day  : {worst_date} ({worst_return:+.2f}% | Z-Score:{worst_z:+.2f})")
    print(f". Live News Sentiment     : {overall_mood} (Net Score: {total_score:+d})")
    print("=" * 60)

if __name__ == "__main__":
    generate_intelligence_report("AAPL")