import numpy as np
import pandas as pd
import riskfolio as rp

from plugIn.optimization.efficient_frontier_base import EfficientFrontierBase


class RiskfolioLibFrontier(EfficientFrontierBase):
    def __init__(self, expected_returns, covariance_matrix, data: pd.DataFrame):
        super().__init__(expected_returns, covariance_matrix, data)
        self.sharpe_ratio = None
        self.volatility = None
        self.expected_return = None
        self.weights = None
        self.port = rp.Portfolio(returns=data.pct_change().dropna())
        # Select method and estimate input parameters:

        method_mu = 'hist'  # Method to estimate expected returns based on historical data.
        method_cov = 'hist'  # Method to estimate covariance matrix based on historical data.
        self.port.assets_stats(method_mu=method_mu, method_cov=method_cov)

        self.model = 'Classic'  # Could be Classic (historical), BL (Black Litterman) or FM (Factor Model)
        self.rm = 'MV'  # Risk measure used, this time will be variance
        self.obj = 'Sharpe'  # Objective function, could be MinRisk, MaxRet, Utility or Sharpe
        self.hist = True  # Use historical scenarios for risk measures that depend on scenarios
        self.rf = 0  # Risk free rate
        self.l = 0  # Risk aversion factor, only useful when obj is 'Utility'

    def calculate_efficient_frontier(self):
        self.weights = self.port.optimization(model=self.model,
                                              rm=self.rm,
                                              obj=self.obj,
                                              rf=self.rf,
                                              l=self.l,
                                              hist=self.hist)

        # Calculate expected return
        # Convert weights and mu to Series or numpy array
        # Convert weights and mu to Series or numpy array
        weights_array = self.weights['weights'].values.flatten()  # Flatten to 1D array
        mu_array = self.port.mu.values.flatten()  # Flatten to 1D array

        # Calculate expected return (dot product of mu and weights)
        self.expected_return = np.dot(mu_array, weights_array)

        # Calculate volatility (weights.T @ cov @ weights)^0.5
        cov_matrix = self.port.cov.values  # Convert covariance matrix to numpy array
        self.volatility = np.sqrt(np.dot(weights_array.T, np.dot(cov_matrix, weights_array)))

        # Calculate Sharpe Ratio (excess return / volatility)
        self.sharpe_ratio = (self.expected_return - self.rf) / self.volatility

    def get_results(self):
        weights_dict = self.weights['weights'].to_dict()
        # Create a new DataFrame with the desired format
        result_df = pd.DataFrame({
            "Cleaned_Weights": [weights_dict],
            "Expected Annual Return": self.expected_return,
            "Annual Volatility": self.volatility,
            "Sharpe Ratio": self.sharpe_ratio
        })
        # print(tabulate(result_df, headers='keys', tablefmt='grid'))
        return result_df
