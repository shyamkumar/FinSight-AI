import yfinance as yf
import pandas as pd


class MarketSentimentAnalyzer:

    def __init__(self):
        pass

    def analyze(self, ticker):

        stock = yf.Ticker(ticker)

        hist = stock.history(period="3mo")

        if hist.empty:

            return None

        current_price = hist["Close"].iloc[-1]

        previous_price = hist["Close"].iloc[0]

        high_price = hist["High"].max()

        low_price = hist["Low"].min()

        avg_volume = hist["Volume"].mean()

        volatility = hist["Close"].pct_change().std() * 100

        price_change = (
            (
                current_price - previous_price
            ) / previous_price
        ) * 100

        # ====================================================
        # MARKET SENTIMENT LOGIC
        # ====================================================

        if price_change > 20:

            sentiment = "Strong Bullish"

            confidence = 94

            signal = "🚀 Strong growth momentum"

        elif price_change > 5:

            sentiment = "Bullish"

            confidence = 84

            signal = "📈 Positive investor sentiment"

        elif price_change > -5:

            sentiment = "Neutral"

            confidence = 72

            signal = "⚖️ Stable market behavior"

        elif price_change > -20:

            sentiment = "Bearish"

            confidence = 64

            signal = "⚠️ Investor uncertainty rising"

        else:

            sentiment = "Strong Bearish"

            confidence = 52

            signal = "🔴 High market pressure"

        return {

            "sentiment": sentiment,

            "confidence": confidence,

            "signal": signal,

            "price_change": round(price_change, 2),

            "current_price": round(current_price, 2),

            "high_price": round(high_price, 2),

            "low_price": round(low_price, 2),

            "avg_volume": int(avg_volume),

            "volatility": round(volatility, 2),

            "history": hist
        }