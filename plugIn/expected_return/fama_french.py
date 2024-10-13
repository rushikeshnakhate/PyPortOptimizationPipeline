from plugIn.expected_return.expected_returns_base import ExpectedReturnBase


class FamaFrenchReturn(ExpectedReturnBase):
    def __init__(self, data):
        super().__init__(data)
        self.risk_free_rate = 0.02  # Example risk-free rate (4%) for demonstration purposes
        self.SMB = 0.02  # Example SMB factor (2%)
        self.HML = 0.01  # Example HML factor (1%)
        self.data = data
        self.tickers = data.columns  # Extract tickers from column names
        self.annualized_return = self.calculate_market_return()

    def calculate_market_return(self):
        """
        Calculate the annualized market return from the data DataFrame.
        :return: Dictionary of annualized returns for each ticker
        """
        annualized_returns = {}
        for ticker in self.tickers:
            # Calculate daily returns
            daily_returns = self.data[ticker].pct_change()
            # Drop NaN values
            daily_returns = daily_returns.dropna()
            # Annualized the return (assuming 252 trading days)
            annualized_return = daily_returns.mean() * 252
            annualized_returns[ticker] = annualized_return
        return annualized_returns

    def calculate_expected_return(self):
        """
        Calculate the expected return based on the Fama-French 3-factor model.
        :return: Dictionary of expected returns for each ticker
        """
        expected_returns = {}
        for ticker in self.tickers:
            market_excess = self.annualized_return[ticker] - self.risk_free_rate
            expected_returns[ticker] = self.risk_free_rate + self.SMB + self.HML + market_excess
        return expected_returns

    def get_annualized_return(self):
        """
        Return the annualized returns for all tickers.
        :return: Dictionary of annualized returns for each ticker
        """
        return self.annualized_return
