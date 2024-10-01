from datetime import datetime

import numpy as np
import pandas as pd
import warnings


class Performance:
    def __init__(self, allocation, price_data, risk_free_rate=0.02):
        """
        Initialize Performance class with allocation and price data.

        :param allocation: Dictionary of stock tickers and the number of shares allocated.
        :param price_data: DataFrame containing historical price data for the stocks.
        :param risk_free_rate: The risk-free rate used for calculating Sharpe Ratio (default is 5%).
        """
        self.allocation = allocation
        self.price_data = price_data
        self.risk_free_rate = risk_free_rate

    def check_dates(self, data, start_date, end_date):
        """Check if start and end dates are in the price data index."""
        missing_dates = [date for date in [start_date, end_date] if date not in self.price_data.index]
        if missing_dates:
            start_date = data.index[0].date().strftime('%Y-%m-%d') if start_date in missing_dates else start_date
            end_date = data.index[-1].date().strftime('%Y-%m-%d') if end_date in missing_dates else end_date

            warnings.warn(
                f"Missing dates in price data: {', '.join(missing_dates)},"
                f"using defaults start_date={start_date},end_data={end_date}")
        return start_date, end_date

    def calculate_return(self, start_date, end_date):
        """Calculate portfolio return over a given time period."""
        try:
            initial_prices = self.price_data.loc[start_date]
            final_prices = self.price_data.loc[end_date]

            initial_value = sum(self.allocation[ticker] * initial_prices[ticker] for ticker in self.allocation)
            final_value = sum(self.allocation[ticker] * final_prices[ticker] for ticker in self.allocation)

            return (final_value - initial_value) / initial_value
        except Exception as e:
            print("error={} for start_date={},end_date{}, ".format(e, start_date, end_date))
            return "error={} for start_date={},end_date{}, ".format(e, start_date, end_date)

    def calculate_volatility(self):
        """Calculate portfolio volatility using daily price data."""
        try:
            daily_returns = self.price_data.pct_change().dropna()
            portfolio_returns = daily_returns[list(self.allocation.keys())].dot(pd.Series(self.allocation))

            return portfolio_returns.std() * np.sqrt(252)  # Annualized volatility
        except Exception as e:
            print("error={} ".format(e))
            return "error={} ".format(e)

    def calculate_sharpe_ratio(self, start_date, end_date):
        """Calculate the Sharpe Ratio of the portfolio over a given time period."""
        try:
            portfolio_return = self.calculate_return(start_date, end_date)
            portfolio_volatility = self.calculate_volatility()

            # Annualized return
            annualized_return = portfolio_return * (252 / len(self.price_data.loc[start_date:end_date]))

            return (annualized_return - self.risk_free_rate) / portfolio_volatility
        except Exception as e:
            print("error={} ".format(e))
            return "error={} ".format(e)


def calculate_performance(allocation_df, data, start_date, end_date):
    """Calculate and append performance metrics for portfolios based on allocation columns."""
    for index, row in allocation_df.iterrows():
        for col in allocation_df.columns:
            if col.startswith('Allocation_') and '_remaining_amount' not in col:
                allocation = row[col]  # Get the allocation dictionary
                performance = Performance(allocation, data)
                start_date, end_date = performance.check_dates(data, start_date, end_date)
                # Calculate performance metrics
                portfolio_return = performance.calculate_return(start_date, end_date)
                portfolio_volatility = performance.calculate_volatility()
                portfolio_sharpe = performance.calculate_sharpe_ratio(start_date, end_date)

                # Append performance metrics to the DataFrame
                method_name = col.split('_')[1]  # Extract method name (Greedy or LP)
                allocation_df.at[index, f'{method_name}_Return'] = portfolio_return
                allocation_df.at[index, f'{method_name}_Volatility'] = portfolio_volatility
                allocation_df.at[index, f'{method_name}_Sharpe'] = portfolio_sharpe

    return allocation_df  # Return the updated DataFrame
