import numpy as np

from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.processing_weight.allocationBase import AllocationBase


@ExecutionTimeRecorder(module_name=__name__)
class CustomWeightedFloorAllocator(AllocationBase):
    def get_allocation(self):
        try:
            total_value = self.total_portfolio_value

            floored_values = {}
            for ticker, weight in self.weights.items():
                # Calculate the number of shares based on the weight, total value, and latest price
                floored_values[ticker] = np.floor(weight * total_value / self.latest_prices[ticker]).astype(int)

            total_floored_value = 0
            for ticker in floored_values:
                total_floored_value += floored_values[ticker] * self.latest_prices[ticker]

            remaining_budget = total_value - total_floored_value

            # Redistribute remaining budget to higher-weighted assets
            if remaining_budget > 0:
                # Order tickers by their original weights (in descending order)
                sorted_tickers = sorted(self.weights, key=self.weights.get, reverse=True)

                for ticker in sorted_tickers:  # Prioritize higher-weighted assets
                    # Calculate the maximum number of shares that can be purchased with the remaining budget
                    max_shares_to_buy = int(remaining_budget // self.latest_prices[ticker])
                    floored_values[ticker] += max_shares_to_buy
                    remaining_budget -= max_shares_to_buy * self.latest_prices[ticker]

                    if remaining_budget <= 0:
                        break  # Exit loop if no remaining budget

            return floored_values, remaining_budget

        except Exception as ex:
            return ex, ex  # Return exception in case of an error
