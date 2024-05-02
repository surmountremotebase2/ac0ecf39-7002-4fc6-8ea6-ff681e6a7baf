from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, BB
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["GME", "AMC", "BBBY"]  # Example meme stocks
        # Optionally, define more data requirements or constraints here

    @property
    def assets(self):
        return self.tickers

    @property
    def interval(self):
        return "1day"  # Daily intervals for assessing conditions

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Calculate technical indicators
            rsi = RSI(ticker, data["ohlcv"], 14)  # Using a 14-day RSI
            bb = BB(ticker, data["ohlcv"], 20, 2)  # 20-period BB with 2 std deviation
            
            if not rsi or not bb:
                log(f"Insufficient data for {ticker}")
                continue

            # Assuming high premiums correlate to RSI > 70 (overbought) and price hitting near upper BB
            recent_rsi = rsi[-1]
            recent_price = data["ohlcv"][-1][ticker]["close"]
            upper_bb = bb["upper"][-1]
            
            is_high_premium_condition = recent_rsi > 70 and recent_price >= upper_bb

            if is_high_premium_condition:
                # Indicate a position, this could be a placeholder indicating a covered call sell signal
                # In actual implementation, you'd need to link this signal to specific option trading actions
                allocation_dict[ticker] = -1  # Placeholder value to indicate selling covered calls
                log(f"Selling covered calls on {ticker} due to high premium conditions")

        if not allocation_dict:
            return TargetAllocation({})  # No action if no conditions are met

        return TargetAllocation(allocation_dict)