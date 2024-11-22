import numpy as np
import pandas as pd

from plugIn.performance_metrics.portfolio_metric_base import PortfolioMetricBase


class PortfolioVolatility(PortfolioMetricBase):
    """Calculates the annualized volatility of the portfolio."""

    def calculate(self, portfolio):
        """
        Calculate annualized portfolio volatility.
        :param portfolio:
        :param **kwargs:
        """
        return self.normalized_volatility(portfolio)
        try:
            keys = list(portfolio.allocation.keys())
            daily_return = portfolio.daily_returns[keys]

            allocations = pd.Series(portfolio.allocation)
            portfolio_weighted_return = daily_return.dot(allocations)
            volatility1 = portfolio_weighted_return.std() * np.sqrt(252)  # Annualized volatility
            return volatility1
        except Exception as ex:
            print("vol1={}".format(ex))

    @staticmethod
    def normalized_volatility(portfolio):
        try:
            keys = list(portfolio.allocation.keys())
            daily_return = portfolio.daily_returns[keys]

            allocations = pd.Series(portfolio.allocation)
            normalized_allocations = allocations / allocations.sum()

            portfolio_weighted_return = daily_return.dot(normalized_allocations)
            volatility2 = portfolio_weighted_return.std() * np.sqrt(252)
            return volatility2
        except Exception as ex:
            raise Exception("calculation fo volatility failed with error={}".format(ex))
