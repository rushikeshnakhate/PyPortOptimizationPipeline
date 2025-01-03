import numpy as np
import pandas as pd
import riskfolio as rp

from src.common.conventions import HeaderConventions
from src.optimization.efficient_frontier_base import EfficientFrontierBase


def make_positive_definite(matrix, epsilon=1e-5):
    """
    Modify a covariance matrix to ensure it is positive definite by
    adding a small value to the diagonal elements until it becomes
    positive definite.

    Args:
        matrix (np.array): Covariance matrix.
        epsilon (float): Small value to add to diagonal elements.

    Returns:
        np.array: Modified positive definite covariance matrix.
    """
    # Try Cholesky decomposition to check if matrix is positive definite
    try:
        # If successful, matrix is already positive definite
        np.linalg.cholesky(matrix)
        return matrix
    except np.linalg.LinAlgError:
        # If not positive definite, add small epsilon to diagonal elements
        diagonal_shift = np.eye(matrix.shape[0]) * epsilon
        return matrix + diagonal_shift


# Base class for risk measure optimization
class RiskFolioOptimizer(EfficientFrontierBase):
    def __init__(self, expected_returns, covariance_matrix, expected_return_type, risk_return_type, output_dir,
                 data: pd.DataFrame, rm: str):
        super().__init__(expected_returns, covariance_matrix, expected_return_type, risk_return_type, output_dir, data)
        self.rm = rm
        self.sharpe_ratio = None
        self.volatility = None
        self.expected_return = None
        self.weights = []
        self.result_df = pd.DataFrame([])

        # Create the Portfolio object from Riskfolio-Lib
        self.port = rp.Portfolio(returns=data.pct_change().dropna())

        # Estimate input parameters for the Portfolio
        method_mu = 'hist'  # Method to estimate expected returns based on historical data.
        method_cov = 'hist'  # Method to estimate covariance matrix based on historical data.
        self.port.assets_stats(method_mu=method_mu, method_cov=method_cov)

        # Ensure covariance matrix is positive definit
        self.port.cov = make_positive_definite(self.port.cov)
        # Optimization parameters
        self.model = 'Classic'  # Could be Classic (historical), BL (Black Litterman) or FM (Factor Model)
        self.obj = 'Sharpe'  # Objective function, could be MinRisk, MaxRet, Utility, or Sharpe
        self.hist = True  # Use historical scenarios for risk measures that depend on scenarios
        self.rf = 0  # Risk-free rate
        self.l = 0  # Risk aversion factor, only useful when obj is 'Utility'

    def calculate_efficient_frontier(self):
        # Perform optimization using the specific risk measure
        self.weights = self.port.optimization(
            model=self.model,
            rm=self.rm,
            obj=self.obj,
            rf=self.rf,
            l=self.l,
            hist=self.hist
        )

        if self.weights is None:
            raise ValueError(
                "Optimization failed: weights returned as None.The problem doesn't have a solution with actual input "
                "parameters")
        # Calculate expected return and volatility
        weights_array = self.weights['weights'].values.flatten()
        mu_array = self.port.mu.values.flatten()
        cov_matrix = self.port.cov.values

        # Define annualization factor for daily returns
        annualization_factor = 252  # Use 252 for daily returns or 12 for monthly returns

        # Calculate expected return as dot product of mu and weights, then annualize it
        self.expected_return = np.dot(mu_array, weights_array) * annualization_factor  # Annualize expected return

        # Calculate volatility: sqrt(weights.T @ cov @ weights), then annualize it
        self.volatility = np.sqrt(np.dot(weights_array.T, np.dot(cov_matrix, weights_array))) * np.sqrt(
            annualization_factor)  # Annualize volatility

        # Calculate Sharpe Ratio
        self.sharpe_ratio = (self.expected_return - self.rf) / self.volatility

    def _get_results(self):
        # Convert weights to a dictionary for storing in DataFrame
        weights_dict = self.weights['weights'].to_dict()

        # Create a temporary DataFrame with calculated values
        result_df = pd.DataFrame({
            HeaderConventions.cleaned_weights_column: [weights_dict],
            HeaderConventions.expected_annual_return_column: [self.expected_return],
            HeaderConventions.annual_volatility_column: [self.volatility],
            HeaderConventions.sharpe_ratio_column: [self.sharpe_ratio]
        })
        return result_df
