import logging
import os
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

from plugIn.conventions import PklFileConventions, HeaderConventions

logger = logging.getLogger(__name__)


# Monte Carlo Simulation Class
class MonteCarloSimulation:
    def __init__(self, data, output_dir, num_of_portfolios=10000):
        self.tickers = data.columns
        self.data = data
        self.num_of_portfolios = num_of_portfolios
        self.log_return = np.log(1 + data.pct_change())
        self.number_of_symbols = len(self.tickers)
        self.simulations_df = None
        self.output_dir = output_dir
        self.pkl_filepath = os.path.join(output_dir, PklFileConventions.monte_carlo_pkl_filename)

    def run_simulation(self, rerun=False):
        """
        Runs the Monte Carlo simulation to generate portfolio weights,
        returns, volatilities, and Sharpe ratios.
        """

        # Check if rerun is required or simulation pickle file exists
        if not rerun and os.path.exists(self.pkl_filepath):
            logger.info(
                "Using previous Monte Carlo Simulation for Portfolio Optimization number of portfolios={}".format(
                    self.num_of_portfolios))
            self.simulations_df = pd.read_pickle(self.pkl_filepath)
        else:
            logger.info(
                "Running Monte Carlo Simulation for Portfolio Optimization number of portfolios={}".format(
                    self.num_of_portfolios))
            self._run_simulation_now()
            self.simulations_df.to_pickle(self.pkl_filepath)

    def _run_simulation_now(self):
        """Private method to run the Monte Carlo simulation."""
        all_weights = np.zeros((self.num_of_portfolios, self.number_of_symbols))
        ret_arr = np.zeros(self.num_of_portfolios)
        vol_arr = np.zeros(self.num_of_portfolios)
        sharpe_arr = np.zeros(self.num_of_portfolios)
        weights_dicts = []
        # Monte Carlo simulations
        for ind in tqdm(range(self.num_of_portfolios), desc="Simulating Portfolios", ncols=100):
            weights = np.random.random(self.number_of_symbols)
            weights /= np.sum(weights)

            # Store the weights
            all_weights[ind, :] = weights

            # Create a dictionary for tickers and their weights
            weights_dict = {self.tickers[i]: weights[i] for i in range(self.number_of_symbols)}
            weights_dicts.append(weights_dict)  # Store the dictionary in the list

            # Calculate expected return, volatility, and Sharpe ratio
            ret_arr[ind] = np.sum((self.log_return.mean() * weights) * 252)
            vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(self.log_return.cov() * 252, weights)))
            sharpe_arr[ind] = ret_arr[ind] / vol_arr[ind]

        weights_df = pd.DataFrame(weights_dicts)
        # Create a DataFrame to store the results
        self.simulations_df = pd.DataFrame({
            HeaderConventions.expected_annual_return_column: ret_arr,
            HeaderConventions.annual_volatility_column: vol_arr,
            HeaderConventions.sharpe_ratio_column: sharpe_arr})

        self.simulations_df[HeaderConventions.weights_column] = weights_dicts

    def _get_portfolio_by(self, criterion=HeaderConventions.sharpe_ratio_column, maximize=True):
        """Helper function to retrieve a portfolio by a specific criterion (e.g., max Sharpe or min volatility)."""
        if self.simulations_df is None:
            raise ValueError("Run the simulation first by calling run_simulation().")

        title: str = None
        if maximize:
            idx = self.simulations_df[criterion].idxmax()
            title = "monte_carlo_max_sharpe_ratio"
        else:
            idx = self.simulations_df[criterion].idxmin()
            title = "monte_carlo_min_annual_volatility"

        selected_portfolio = self.simulations_df.loc[idx].copy()
        selected_portfolio[HeaderConventions.expected_return_column] = title
        selected_portfolio[HeaderConventions.risk_model_column] = title
        selected_portfolio[HeaderConventions.optimizer_column] = title
        return pd.DataFrame(selected_portfolio).T

    def get_max_sharpe_ratio(self):
        """Retrieve the portfolio with the maximum Sharpe ratio."""
        return self._get_portfolio_by(criterion=HeaderConventions.sharpe_ratio_column, maximize=True)

    def get_min_volatility(self):
        """Retrieve the portfolio with the minimum volatility."""
        return self._get_portfolio_by(criterion=HeaderConventions.annual_volatility_column, maximize=False)

    def run_monte_carlo_simulation(self):
        """Run the Monte Carlo Simulation and return max Sharpe ratio and min volatility portfolios."""
        self.run_simulation()
        return self.get_max_sharpe_ratio(), self.get_min_volatility()


def run_monte_carlo_simulation(output_dir, data):
    """
    Run the Monte Carlo simulation and append the results to the results DataFrame.
    """
    monte_carlo_df = pd.DataFrame()
    monte_carlo_simulation = MonteCarloSimulation(data, output_dir)
    max_sharpe_ratio, min_volatility = monte_carlo_simulation.run_monte_carlo_simulation()
    monte_carlo_df = pd.concat([monte_carlo_df, max_sharpe_ratio], ignore_index=True)
    monte_carlo_df = pd.concat([monte_carlo_df, min_volatility], ignore_index=True)
    pkl_output_path = os.path.join(output_dir, PklFileConventions.short_listed_monte_carlo_pkl_filename)
    monte_carlo_df.to_pickle(pkl_output_path)
    return monte_carlo_df
