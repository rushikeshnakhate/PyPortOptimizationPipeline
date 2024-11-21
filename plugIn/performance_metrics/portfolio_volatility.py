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
        portfolio_returns = portfolio.daily_returns[list(portfolio.allocation.keys())].dot(
            pd.Series(portfolio.allocation))
        return portfolio_returns.std() * np.sqrt(252)  # Annualized volatility
