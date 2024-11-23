from abc import ABC, abstractmethod


class AllocationBase(ABC):
    def __init__(self, weights, latest_prices, total_portfolio_value=10000, short_ratio=None):
        self.weights = weights
        self.latest_prices = latest_prices
        self.total_portfolio_value = total_portfolio_value
        self.short_ratio = short_ratio

    @abstractmethod
    def get_allocation(self):
        pass
