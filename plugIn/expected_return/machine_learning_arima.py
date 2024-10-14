import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.expected_return.expected_returns_base import ExpectedReturnBase


class ARIMAReturn(ExpectedReturnBase):
    def __init__(self, data):
        super().__init__(data)
        self.data = data
        self.data.index = pd.to_datetime(data.index)
        self.data = data.asfreq('B')  # Business day frequency
        # self.expected_returns = self.calculate_expected_return()

    @ExecutionTimeRecorder(module_name=__name__)  # Use __name__ to get the module name
    def calculate_expected_return(self):
        """
        Calculate the expected return based on ARIMA model for each ticker.
        :return: Dictionary of annualized expected returns for each ticker
        """
        # Check if cached values exist
        # cached_returns = self._load_cache()
        # if cached_returns is not None:
        #     return cached_returns

        expected_returns = {}
        tickers = self.data.columns

        # Iterate over each ticker
        for ticker in tickers:
            # Fit ARIMA model (order (5, 1, 0) is a typical ARIMA model configuration)
            model = ARIMA(self.data[ticker], order=(5, 1, 0))
            model_fit = model.fit()
            # Forecast the next period's return (e.g., next day)
            daily_return_forecast = model_fit.forecast(steps=1)[0]
            # Get the current (last available) price
            current_price = self.data[ticker].iloc[-1]
            # Calculate daily expected return
            daily_return = (daily_return_forecast - current_price) / current_price
            # Convert daily return to annualized return
            annualized_return = (1 + daily_return) ** 252 - 1
            expected_returns[ticker] = annualized_return

        return expected_returns
