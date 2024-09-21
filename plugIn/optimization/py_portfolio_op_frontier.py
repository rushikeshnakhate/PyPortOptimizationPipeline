import pandas as pd
from pypfopt import EfficientFrontier

from plugIn.optimization.efficient_frontier_base import EfficientFrontierBase


class PyPortfolioOptFrontier(EfficientFrontierBase):
    def __init__(self, expected_returns, covariance_matrix, data=None):
        super().__init__(expected_returns, covariance_matrix, data)
        self.weights = None
        self.ef = None

    def calculate_efficient_frontier(self):
        self.ef = EfficientFrontier(self.expected_returns, self.covariance_matrix)
        self.weights = self.ef.max_sharpe()
        self.cleaned_weights = dict(self.ef.clean_weights())
        self.performance = self.ef.portfolio_performance(verbose=False)

    def get_results(self):
        # Create a DataFrame for performance metrics
        result_df = pd.DataFrame({
            "Cleaned_Weights": [self.cleaned_weights],
            "Expected Annual Return": [self.performance[0]],
            "Annual Volatility": [self.performance[1]],
            "Sharpe Ratio": [self.performance[2]]
        })
        return result_df

