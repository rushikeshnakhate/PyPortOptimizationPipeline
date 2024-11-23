from pypfopt import DiscreteAllocation

from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.processing_weight.allocationBase import AllocationBase


class GreedyPortfolio(AllocationBase):
    def __init__(self, weights, latest_prices, total_portfolio_value=10000, short_ratio=None):
        super().__init__(weights, latest_prices, total_portfolio_value, short_ratio)
        self.discreteAllocation = None

    @ExecutionTimeRecorder(module_name=__name__)
    def get_allocation(self):
        self.discreteAllocation = DiscreteAllocation(
            self.weights,
            self.latest_prices,
            total_portfolio_value=self.total_portfolio_value,
            short_ratio=self.short_ratio
        )
        return self.discreteAllocation.greedy_portfolio()
