import numpy as np

from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.processing_weight.allocationBase import AllocationBase


@ExecutionTimeRecorder(module_name=__name__)
class CustomTransactionCostAllocator(AllocationBase):
    def __init__(self, weights, latest_prices, total_portfolio_value=100000, short_ratio=None,
                 transaction_cost_rate=0.005):
        super().__init__(weights, latest_prices, total_portfolio_value, short_ratio)
        self.transaction_cost_rate = transaction_cost_rate

    def get_allocation(self):
        try:
            total_value = self.total_portfolio_value

            # Adjust weights for transaction costs
            adjusted_weights = {
                ticker: weight * (1 - self.transaction_cost_rate) for ticker, weight in self.weights.items()
            }

            # Calculate allocation for each ticker
            scaled_values = {}
            total_allocated_value = 0  # Track total allocated value
            for ticker, adjusted_weight in adjusted_weights.items():
                # Calculate number of shares (rounded) for each ticker
                shares = np.floor(adjusted_weight * total_value / self.latest_prices[ticker]).astype(int)
                scaled_values[ticker] = shares
                total_allocated_value += shares * self.latest_prices[ticker]

            # Calculate the remaining budget
            remaining_budget = total_value - total_allocated_value

            return scaled_values, remaining_budget
        except Exception as ex:
            return ex, ex  # Return exception in case of an error
