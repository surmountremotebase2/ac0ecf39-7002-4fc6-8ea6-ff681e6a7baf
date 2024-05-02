from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, News
from surmount.logging import log
import pandas as pd

class TradingStrategy(Strategy):
    def __init__(self):
        # List of ticker symbols for major Canadian banks
        self.tickers = ['RY', 'TD', 'BNS', 'BMO', 'CM', 'NA']
        # Assuming 'News' data source is available for checking news related to the stocks
        self.data_list = [News(ticker) for ticker in self.tickers]
        self.underperformance_threshold = 0.05  # 5% lag considered significant

    @property
    def interval(self):
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Fetch closing prices for each ticker
        closes = {ticker: data["ohlcv"][-1][ticker]['close'] for ticker in self.tickers}

        # Calculate average closing price
        average_close = sum(closes.values()) / len(closes)

        # Dictionary to hold the target allocation
        allocation_dict = {}

        for ticker in self.tickers:
            # Check for news
            news_data = data.get(('news', ticker), [])
            recent_news = False

            # Assuming 'publishedDate' and 'sentiment' are keys in the news items
            for news_item in news_data:
                if news_item['sentiment'] < 0:  # Basic filter for potentially negative news impacting the stock
                    recent_news = True
                    break

            # Calculate performance difference from the average
            performance_gap = (closes[ticker] - average_close) / average_close

            # If the stock is lagging significantly without recent negative news, allocate to buy
            if performance_gap < -self.underperformance_threshold and not recent_news:
                allocation_dict[ticker] = 1.0 / len([t for t in self.tickers if t != ticker])  # Simple equal weight
            else:
                allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)