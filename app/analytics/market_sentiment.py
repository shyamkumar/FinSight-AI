import yfinance as yf


class MarketSentimentAnalyzer:

    def __init__(self):
        pass

    def analyze(self, ticker):

        stock = yf.Ticker(ticker)

        hist = stock.history(period="1mo")

        current_price = hist["Close"].iloc[-1]

        previous_price = hist["Close"].iloc[0]

        price_change = (
            (
                current_price - previous_price
            ) / previous_price
        ) * 100

        # ============================================
        # MARKET SENTIMENT
        # ============================================

        if price_change > 10:

            sentiment = "Strong Bullish"

            confidence = 92

        elif price_change > 0:

            sentiment = "Bullish"

            confidence = 81

        elif price_change > -10:

            sentiment = "Bearish"

            confidence = 68

        else:

            sentiment = "Strong Bearish"

            confidence = 55

        return {

            "sentiment": sentiment,

            "confidence": confidence,

            "price_change": round(price_change, 2)
        }