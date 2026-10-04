# That's one way
# import yfinance as yf
# from datetime import datetime

# def get_stock_news(ticker="AAPL", limit=5):
#     print(f"🗞️ Fetching recent financial news for {ticker}...")
#     stock = yf.Ticker(ticker)
#     # Creates a connection to ticker which is "AAPL"
#     news_items = stock.news
#     # .news reaches out to yahoo finance and pulls out the most recent news
#     # and saved into news_items which is memory of computer

#     if not news_items: 
#         print("No recent news items found.")
#         return []
    
#     print(f" Found {len(news_items)} total news stories. Showing top {limit}:\n")

#     formatted_news = []
#     for i, item in enumerate(news_items[:limit], 1):
#     # enumerate is the builtin python lib it basically tells us the position/index number of the item on what we're looping through
#         content = item.get("content", {})
#         # .get(content) is safely asking yfinance is there any content in your lib if yes then give it to me if not then is there any keyword which matches content?
#         title = content.get("title") or item.get("title", "No Title")
#         # it's just 2 ways of getting the title if one works then ok or else use another 
#         publisher = content.get("provider", {}).get("displayName") or item.get("publisher", "unknown publisher")

#         print(f"{i}. [{publisher}] {"title": title}")
    
#     return formatted_news

# if __name__ == "__main__":
#     get_stock_news()

# That's another better way
import requests

def get_stock_news(ticker="AAPL", limit=5):
    print(f"🗞️ Fetching live financial news for {ticker}...")

    # 1. Direct endpoint to yahoofinance news api
    url = f"https://query2.finance.yahoo.com/v1/finance/search?q={ticker}"

    # 2. Add a standard user-agent header so server recognizes us as a real client
    headers = {
        "User-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to fetch news. HTTP Status Code: {response.status_code}")
        return []

    data = response.json()
    news_items = data.get("news", [])

    if not news_items: 
        print(f"No recent news items found for {ticker}.")
        return []

    print(f"✅ Found {len(news_items)} total stories. Showing top {limit}:\n")

    formatted_news = []
    for i, item in enumerate(news_items[:limit], 1):
        title = item.get("title", "No Title")
        publisher = item.get("publisher", "unknown publisher")
        link = item.get("link", "")

        print(f"{i}. [{publisher}] {title}")
        formatted_news.append({
            "title": title,
            "publisher": publisher,
            "link": link
        })

    return formatted_news

if __name__ == "__main__":
    get_stock_news()
