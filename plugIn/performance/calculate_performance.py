import datetime
import logging
import warnings

import numpy as np
import pandas as pd


class BasePerformance:
    def __init__(self, allocation, price_data, remaining_amount=0, total_capital=1000000, risk_free_rate=0.02):
        """
        Base class for portfolio performance calculation.

        :param allocation: Dictionary of stock tickers and the number of shares allocated.
        :param price_data: DataFrame containing historical price data for the stocks.
        :param remaining_amount: The remaining unallocated capital.
        :param total_capital: Total capital available for the portfolio.
        :param risk_free_rate: The risk-free rate used for calculating Sharpe Ratio (default is 2%).
        """
        self.allocation = eval(allocation) if isinstance(allocation,
                                                         str) else allocation  # Convert string to dictionary
        self.price_data = price_data
        self.remaining_amount = remaining_amount
        self.total_capital = total_capital
        self.risk_free_rate = risk_free_rate

    def check_dates(self, start_date, end_date):
        """Check if start and end dates are in the price data index."""
        # self.price_data.index = pd.to_datetime(self.price_data.index).date
        start_date = pd.to_datetime(start_date).date()
        end_date = pd.to_datetime(end_date).date()

        if start_date not in self.price_data.index:
            # logging.warn(
            #     f"Start date {start_date} is not present in the price data. Using the first available date{self.price_data.index[0]}.")
            start_date = self.price_data.index[0]  # Use first available date

        if end_date not in self.price_data.index:
            # logging.warn(
            #     f"End date {end_date} is not present in the price data. Using the last available date{self.price_data.index[-1]}.")
            end_date = self.price_data.index[-1]  # Use last available date
        return start_date, end_date

    def calculate_return(self, start_date, end_date):
        """Calculate portfolio return over a given time period."""
        try:
            # print(f"start_date={start_date}, end_date={end_date}")
            initial_prices = self.price_data.loc[start_date]
            final_prices = self.price_data.loc[end_date]
            # # # Adjust for remaining amount
            allocated_amount = self.total_capital - self.remaining_amount
            allocation_proportion = allocated_amount / self.total_capital

            initial_value = sum(self.allocation[ticker] * initial_prices[ticker] for ticker in self.allocation)
            final_value = sum(self.allocation[ticker] * final_prices[ticker] for ticker in self.allocation)

            return allocation_proportion * ((final_value - initial_value) / initial_value)
        except Exception as e:
            print(f"Error: {e} for start_date={start_date}, end_date={end_date}")
            return None

    def calculate_volatility(self):
        """Calculate portfolio volatility using daily price data."""
        try:
            daily_returns = self.price_data.pct_change().dropna()
            portfolio_returns = daily_returns[list(self.allocation.keys())].dot(pd.Series(self.allocation))

            return portfolio_returns.std() * np.sqrt(252)  # Annualized volatility
        except Exception as e:
            print(f"Error in calculate_volatility: {e}")
            return None

    def calculate_sharpe_ratio(self, start_date, end_date):
        """Calculate the Sharpe Ratio of the portfolio over a given time period."""
        try:
            portfolio_return = self.calculate_return(start_date, end_date)
            portfolio_volatility = self.calculate_volatility()

            # Annualized return
            if portfolio_return is not None and portfolio_volatility is not None:
                # Remove timezone information from the index
                self.price_data.index = self.price_data.index.tz_localize(None)
                # Ensure start_date and end_date are also timezone-naive
                start_date = pd.to_datetime(start_date).tz_localize(None)
                end_date = pd.to_datetime(end_date).tz_localize(None)

                # Now the dates are all tz-naive and can be compared
                annualized_return = portfolio_return * (252 / len(self.price_data.loc[start_date:end_date]))
                return (annualized_return - self.risk_free_rate) / portfolio_volatility
            else:
                return None
        except Exception as e:
            print(f"Error in calculate_sharpe_ratio: {e}")
            return None


class DefaultPerformance(BasePerformance):
    """Default performance calculation class inheriting from BasePerformance."""

    def __init__(self, allocation, price_data, remaining_amount=0):
        super().__init__(allocation, price_data, remaining_amount)

# Example usage:
# df = pd.read_csv('your_dataframe.csv')  # Replace with your actual DataFrame
# data = pd.read_csv('your_price_data.csv', index_col='Date')  # Example price data
# total_capital = 10000  # Total capital
# start_date = '2023-01-01'
# end_date = '2023-12-31'
# result_df = calculate_performance(df, data, start_date, end_date)
