import numpy as np

from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.expected_return.expected_returns_base import ExpectedReturnBase


class RiskParityReturn(ExpectedReturnBase):
    def __init__(self, data):
        self.data = data

    def calculate_covariance_matrix(self):
        """
        Calculate the covariance matrix of asset returns.
        :return: Covariance matrix
        """
        returns = self.data.pct_change().dropna()
        covariance_matrix = returns.cov()
        return covariance_matrix

    def calculate_risk_contributions(self, covariance_matrix):
        """
        Calculate the risk contributions of each asset.
        :param covariance_matrix: Covariance matrix of asset returns
        :return: Dictionary of risk contributions for each asset
        """
        # Calculate the portfolio's variance
        num_assets = len(covariance_matrix)
        weights = np.ones(num_assets) / num_assets
        portfolio_variance = np.dot(weights.T, np.dot(covariance_matrix, weights))

        # Calculate the risk contribution for each asset
        risk_contributions = {}
        for i in range(num_assets):
            asset_covariance = covariance_matrix.iloc[i, :]
            contribution = (weights[i] * np.dot(asset_covariance, weights)) / portfolio_variance
            risk_contributions[self.data.columns[i]] = contribution
        return risk_contributions

    def calculate_weights_based_on_risk(self, risk_contributions):
        """
        Calculate the portfolio weights based on risk contributions.
        :param risk_contributions: Dictionary of risk contributions for each asset
        :return: Dictionary of portfolio weights for each asset
        """
        total_risk_contribution = sum(risk_contributions.values())
        weights = {ticker: (1 / contribution) / total_risk_contribution for ticker, contribution in
                   risk_contributions.items()}
        return weights

    @ExecutionTimeRecorder(module_name=__name__)  # Use __name__ to get the module name
    def _calculate_expected_return(self):
        """
        Calculate the expected return based on risk parity approach.
        :return: Dictionary of expected returns for each asset
        """
        covariance_matrix = self.calculate_covariance_matrix()
        risk_contributions = self.calculate_risk_contributions(covariance_matrix)
        weights = self.calculate_weights_based_on_risk(risk_contributions)

        # Calculate expected return based on these weights
        returns = self.data.pct_change().dropna().mean() * 252  # Annualize returns
        return self._convert_to_dataframe(returns)
