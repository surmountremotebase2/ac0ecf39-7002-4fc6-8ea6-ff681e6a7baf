from surmount.base_class import Strategy, TargetAllocation
from surmount.data import EffectiveFederalFundsRate

class TradingStrategy(Strategy):
    def __init__(self):
        # Assume the symbol for a long-term bond ETF, e.g., TLT for 20+ Year Treasury Bond ETF
        self.tickers = ["TLT"]
        # Add EffectiveFederalFundsRate data to monitor for interest rate cut signals
        self.data_list = [EffectiveFederalFundsRate()]

    @property
    def interval(self):
        # Use a daily interval for this strategy
        return "1day"

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        # Initialize allocation to 0, meaning not holding the ETF
        allocation_dict = {self.tickers[0]: 0}
        
        # Retrieve the Effective Federal Funds Rate data
        fed_funds_rate_data = data[("effective_federal_funds_rate",)]
        
        if len(fed_funds_rate_data) > 2:
            # Compare the latest two rates to see if there's a declining trend indicating potential rate cuts
            latest_rate = fed_funds_rate_data[-1]["value"]
            previous_rate = fed_funds_rate_data[-2]["value"]
            
            # If the latest rate has decreased compared to the previous, increase allocation to the bond ETF
            if latest_rate < previous_rate:
                # This indicates the possibility of a future rate cut, which generally benefits long-term bonds
                allocation_dict[self.tickers[0]] = 1  # Allocate fully to TLT
            else:
                allocation_dict[self.tickers[0]] = 0  # Stay out of the market
            
        return TargetAllocation(allocation_dict)