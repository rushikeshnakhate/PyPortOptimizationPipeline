import numpy as np
from sklearn.linear_model import LinearRegression

from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.expected_return.expected_returns_base import ExpectedReturnBase


class LinearRegressionReturn(ExpectedReturnBase):
    def __init__(self, data):
        super().__init__(data)
        self.data = data
        self.expected_returns = self.calculate_expected_return()

    @ExecutionTimeRecorder(module_name=__name__)  # Use __name__ to get the module name
    def calculate_expected_return(self):
        """
        Calculate the expected return based on linear regression for each ticker.
        :return: Dictionary of annualized expected returns for each ticker
        """
        expected_returns = {}
        tickers = self.data.columns

        # Iterate over each ticker
        for ticker in tickers:
            # Calculate daily returns
            returns = self.data[ticker].pct_change().dropna()

            # Prepare time steps as features (X) and returns as target (y)
            X = np.arange(len(returns)).reshape(-1, 1)  # Time steps (0, 1, 2, ...) as features
            y = returns.values  # Target variable: percentage returns

            # Fit the linear regression model
            model = LinearRegression()
            model.fit(X, y)

            # Predict the expected return for the next period (future time step)
            next_time_step = [[len(returns)]]  # The next time step
            predicted_daily_return = model.predict(next_time_step)[0]  # Daily expected return

            # Convert the predicted daily return to an annualized return
            annualized_return = (1 + predicted_daily_return) ** 252 - 1  # Annualized return for daily data

            # Store the expected return
            expected_returns[ticker] = annualized_return

        return expected_returns
