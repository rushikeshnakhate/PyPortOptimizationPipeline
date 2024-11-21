# Metric: Portfolio Return
from plugIn.performance_metrics.portfolio_metric_base import PortfolioMetricBase


class PortfolioReturn(PortfolioMetricBase):
    def __init__(self, config=None):
        super().__init__(config)
        if config is None:
            raise Exception("expected start_date,end_date to calculate PortfolioReturn, but not provided")
        self.start_date = self.config.get('start_date')
        self.end_date = self.config.get('end_date')

    def calculate(self, portfolio):
        """
        Calculate portfolio return between two dates.
        0"""
        start_date, end_date = portfolio.check_dates(self.start_date, self.end_date)
        initial_prices = portfolio.price_data.loc[start_date]
        final_prices = portfolio.price_data.loc[end_date]

        initial_value = sum(
            portfolio.allocation[ticker] * initial_prices[ticker] for ticker in portfolio.allocation
        )
        final_value = sum(
            portfolio.allocation[ticker] * final_prices[ticker] for ticker in portfolio.allocation
        )

        allocated_amount = portfolio.total_capital - portfolio.remaining_amount
        allocation_proportion = allocated_amount / portfolio.total_capital

        return allocation_proportion * ((final_value - initial_value) / initial_value)
