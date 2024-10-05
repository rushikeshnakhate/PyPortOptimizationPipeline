import pandas as pd
from pypfopt import EfficientFrontier

from plugIn.conventions import HeaderConventions
from plugIn.optimization.efficient_frontier_base import EfficientFrontierBase


class PyPortfolioOptFrontierBase(EfficientFrontierBase):
    def __init__(self, expected_returns, covariance_matrix, data=None, weight_bounds=(0, 1)):
        super().__init__(expected_returns, covariance_matrix, data)
        self.weights = None
        self.ef = None
        self.weight_bounds = weight_bounds  # Add weight bounds as an instance attribute

    def calculate_efficient_frontier(self):
        # Use the weight bounds during initialization
        self.ef = EfficientFrontier(self.expected_returns, self.covariance_matrix, weight_bounds=self.weight_bounds)
        self.weights = self.ef.max_sharpe()  # Max Sharpe optimization
        self.cleaned_weights = dict(self.ef.clean_weights())  # Clean the weights
        self.performance = self.ef.portfolio_performance(verbose=False)  # Portfolio performance

    def get_results(self):
        # Create a DataFrame for performance metrics
        result_df = pd.DataFrame({
            HeaderConventions.cleaned_weights_column: [self.cleaned_weights],
            HeaderConventions.expected_annual_return_column: [self.performance[0]],
            HeaderConventions.annual_volatility_column: [self.performance[1]],
            HeaderConventions.sharpe_ratio_column: [self.performance[2]]
        })
        return result_df


class PyPortfolioOptFrontier(PyPortfolioOptFrontierBase):
    def __init__(self, expected_returns, covariance_matrix, data=None):
        # Call the base class with default weight bounds (0, 1)
        super().__init__(expected_returns, covariance_matrix, data, weight_bounds=(0, 1))


class PyPortfolioOptFrontierWithShortPosition(PyPortfolioOptFrontierBase):
    def __init__(self, expected_returns, covariance_matrix, data=None):
        # Call the base class with weight bounds allowing short positions (-1, 1)
        super().__init__(expected_returns, covariance_matrix, data, weight_bounds=(-1, 1))
