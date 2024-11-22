import numpy as np

from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.processing_weight.allocationBase import AllocationBase


@ExecutionTimeRecorder(module_name=__name__)
class ProportionalRoundingAllocator(AllocationBase):
    def get_allocation(self):
        total_value = self.total_portfolio_value
        proportionate_values = {ticker: np.round(weight * total_value) for ticker, weight in self.weights.items()}

        # Sum of rounded allocations
        total_allocated = sum(proportionate_values.values())

        # Calculate remaining budget (difference between total value and allocated amount)
        remaining_budget = total_value - total_allocated

        # Sort tickers by their original weights in descending order
        error_idx = sorted(self.weights, key=self.weights.get, reverse=True)

        # Adjust for rounding errors by proportionally distributing the remaining budget
        for ticker in error_idx:
            if remaining_budget > 0:
                proportionate_values[ticker] += 1
                remaining_budget -= self.latest_prices[ticker]
            elif remaining_budget < 0:
                proportionate_values[ticker] -= 1
                remaining_budget += self.latest_prices[ticker]

        # Convert the values to integers before returning the allocation
        resu = {ticker: int(value) for ticker, value in proportionate_values.items()}
        return resu, remaining_budget
