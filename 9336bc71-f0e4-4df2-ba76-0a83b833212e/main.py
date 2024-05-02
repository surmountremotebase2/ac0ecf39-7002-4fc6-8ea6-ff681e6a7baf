from surmount.base_class import Strategy, TargetAllocation
from surmount.logging import log
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Assuming the assets have a format that distinguishes between different exchanges for the same ticker
        # For example, "AAPL:NASDAQ" and "AAPL:NYSE" could represent Apple on two different exchanges
        self.arbitrage_pairs = [("AAPL:NASDAQ", "AAPL:NYSE"), ("MSFT:NASDAQ", "MSFT:NYSE")]
        
    @property
    def interval(self):
        # The frequency of checks can be adjusted based on strategy needs
        return "1min"

    @property
    def assets(self):
        # Flattening the list of arbitrage pair tuples to get a unique list of asset identifiers
        return list(set([asset for pair in self.arbitrage_pairs for asset in pair]))

    @property
    def data(self):
        # We are only interested in the latest prices, no additional data needed for this strategy
        return []

    def run(self, data):
        allocation_dict = {}
        for pair in self.arbitrage_pairs:
            asset_1, asset_2 = pair
            price_1 = data["ohlcv"][-1][asset_1]["close"] # Latest closing price for asset 1
            price_2 = data["ohlcv"][-1][asset_2]["close"] # Latest closing price for asset 2
            discrepancy = abs(price_1 - price_2) / min(price_1, price_2)
            
            # Log for debugging
            log(f"Discrepancy between {asset_1} and {asset_2}: {discrepancy*100:.2f}%")
            
            # If the price discrepancy is at least 5%, we consider it an arbitrage opportunity
            if discrepancy >= 0.05:
                # Arbitrage logic:
                # Buy on the exchange with the lower price and sell on the exchange with the higher price
                if price_1 < price_2:
                    # Buy asset_1, sell asset_2
                    allocation_dict[asset_1] = 1.0  # This represents a full allocation to buying asset_1; 
                                                     # the exact mechanism to sell asset_2 might depend on Surmount AI's capabilities
                    # In a real-world scenario, one would also need to consider transaction costs, exchange fees, and slippage.
                else:
                    # Buy asset_2, sell asset_1
                    allocation_dict[asset_2] = 1.0  # Similarly, this represents buying asset_2 fully
                    
                # In an actual implementation, sophisticated handling to manage allocations and not exceed 100% of capital would be needed
                
        return TargetAllocation(allocation_dict)