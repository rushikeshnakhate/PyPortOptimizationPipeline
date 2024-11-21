import pandas as pd


class PortfolioWithAllocatedWeights:
    def __init__(self, allocation, price_data, remaining_amount=0, total_capital=1_000_000, risk_free_rate=0.02):
        """
        Portfolio Class: Stores allocation, price data, and portfolio-related information.

        :param allocation: Dictionary of stock tickers and the number of shares allocated.
        :param price_data: DataFrame containing historical price data for the stocks.
        :param remaining_amount: The remaining unallocated capital.
        :param total_capital: Total capital available for the portfolio.
        :param risk_free_rate: The risk-free rate (default is 2%).
        """
        self.allocation = allocation if isinstance(allocation, dict) else eval(allocation)
        self.price_data = price_data
        self.remaining_amount = remaining_amount
        self.total_capital = total_capital
        self.risk_free_rate = risk_free_rate

        # Pre-compute daily returns
        self.daily_returns = self.price_data.pct_change().dropna()

    def check_dates(self, start_date, end_date):
        """
        Ensure the start and end dates are valid and exist in the price data.
        """
        start_date = pd.to_datetime(start_date).date()
        end_date = pd.to_datetime(end_date).date()

        if start_date not in self.price_data.index:
            start_date = self.price_data.index[0]

        if end_date not in self.price_data.index:
            end_date = self.price_data.index[-1]

        return start_date, end_date
