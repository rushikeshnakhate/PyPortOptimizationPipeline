from statsmodels.tsa.holtwinters import ExponentialSmoothing

from plugIn.expected_return.expected_returns_base import ExpectedReturnBase


class HoltWintersReturn(ExpectedReturnBase):
    def __init__(self, data):
        super().__init__(data)
        self.data = data

    def calculate_expected_return(self):
        """
        Calculate the expected return using Holt-Winters Exponential Smoothing.
        :return: Dictionary of expected returns for each ticker
        """
        expected_returns = {}
        # Calculate percentage returns
        returns = self.data.pct_change().dropna()

        for ticker in returns.columns:
            series = returns[ticker]
            model = ExponentialSmoothing(series, trend='add', seasonal='add', seasonal_periods=12)
            fit_model = model.fit()
            forecast = fit_model.forecast(1)
            expected_returns[ticker] = forecast.values[0] * 252  # Annualized the daily return
        return expected_returns
