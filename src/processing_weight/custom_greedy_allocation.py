import numpy as np

from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.processing_weight.allocationBase import AllocationBase


@ExecutionTimeRecorder(module_name=__name__)
class CustomGreedyAllocation(AllocationBase):
    def __init__(self, weights, latest_prices, total_portfolio_value=10000, short_ratio=None):

        self.discreteAllocation = None
        if isinstance(weights, dict):
            self.weights = np.array(list(weights.values()))
        else:
            self.weights = np.array(weights)
        super().__init__(self.weights, latest_prices, total_portfolio_value, short_ratio)

    def get_allocation(self):
        shares = [0] * len(self.weights)
        remaining_budget = self.total_portfolio_value

        for i in np.argsort(-self.weights):  # Sort by descending weights
            max_shares = int(remaining_budget // self.latest_prices[i])
            shares[i] = max_shares
            remaining_budget -= max_shares * self.latest_prices[i]
            if remaining_budget < 0:
                break

        return shares
