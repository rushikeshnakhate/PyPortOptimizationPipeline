import logging

import pandas as pd

from src.performance_metrics.performance_metrics_name_convernsions import PerformanceMetricsNameConventions
from src.performance_metrics.portfolio_metric_base import PortfolioMetricBase

logger = logging.getLogger(__name__)


class PortfolioSharpeRatio(PortfolioMetricBase):
    def __init__(self, config=None):
        super().__init__(config)
        self.start_date = self.config.get('start_date')
        self.end_date = self.config.get('end_date')

    def calculate(self, portfolio, precalculated_metrics):
        """
        Calculate Sharpe Ratio.
        """
        # Use other metrics to compute required components
        # Annualize return

        portfolio_return = precalculated_metrics.get(PerformanceMetricsNameConventions.portfolio_return)
        portfolio_volatility = precalculated_metrics.get(PerformanceMetricsNameConventions.portfolio_volatility)

        portfolio.price_data.index = portfolio.price_data.index.tz_localize(None)
        # Ensure start_date and end_date are also timezone-naive
        start_date = pd.to_datetime(self.start_date).tz_localize(None)
        end_date = pd.to_datetime(self.end_date).tz_localize(None)

        # Now the dates are all tz-naive and can be compared
        annualized_return = portfolio_return * (252 / len(portfolio.price_data.loc[start_date:end_date]))
        return (annualized_return - portfolio.risk_free_rate) / portfolio_volatility
