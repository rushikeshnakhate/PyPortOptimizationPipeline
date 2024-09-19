import os
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm


#  Monte Carlo Simulation
class MonteCarloSimulation:
    def __init__(self, tickers, data, num_of_portfolios=5000):
        """
        Initializes the Monte Carlo Simulation class.

        :param tickers: List of stock symbols.
        :param data: DataFrame of stock price data.
        :param num_of_portfolios: Number of portfolios to simulate (default is 5000).
        """
        self.tickers = tickers
        self.data = data
        self.num_of_portfolios = num_of_portfolios
        self.log_return = np.log(1 + data.pct_change())
        self.number_of_symbols = len(tickers)
        self.simulations_df = None

    def run_simulation(self, rerun=False):
        """
        Runs the Monte Carlo simulation to generate portfolio weights,
        returns, volatilises, and Sharpe ratios.

        :return: DataFrame of simulated portfolios with Returns, Volatility, Sharpe Ratio, and Portfolio Weights.
        """
        # Initialize arrays to store results
        if rerun is False:
            output_dir = Path(r"D:\PortOpt\data")
            pkl_filepath = os.path.join(output_dir, "simulation.pkl")
            if not os.path.exists(pkl_filepath):
                self.run_simulation_now()
                self.simulations_df.to_pickle(pkl_filepath)
            else:
                self.simulations_df = pd.read_pickle(pkl_filepath)
            return self.simulations_df

    # This method is private and should not be called directly by the submodules
    def run_simulation_now(self):
        all_weights = np.zeros((self.num_of_portfolios, self.number_of_symbols))
        ret_arr = np.zeros(self.num_of_portfolios)
        vol_arr = np.zeros(self.num_of_portfolios)
        sharpe_arr = np.zeros(self.num_of_portfolios)

        # Start the Monte Carlo simulations
        for ind in tqdm(range(self.num_of_portfolios), desc="Simulating Portfolios", ncols=100):
            # Randomly generate weights
            weights = np.random.random(self.number_of_symbols)
            weights /= np.sum(weights)

            # Store the weights
            all_weights[ind, :] = weights

            # Calculate expected return
            ret_arr[ind] = np.sum((self.log_return.mean() * weights) * 252)

            # Calculate portfolio volatility
            vol_arr[ind] = np.sqrt(np.dot(weights.T, np.dot(self.log_return.cov() * 252, weights)))

            # Calculate Sharpe Ratio
            sharpe_arr[ind] = ret_arr[ind] / vol_arr[ind]

        # Create a DataFrame to store the results
        self.simulations_df = pd.DataFrame({
            'Returns': ret_arr,
            'Volatility': vol_arr,
            'SharpeRatio': sharpe_arr,
            'PortfolioWeights': [list(weights) for weights in all_weights]
        })

    def get_max_sharpe_ratio(self):
        """
        Retrieves the portfolio with the maximum Sharpe Ratio.
        :return: Dictionary of portfolio weights and expected return for the max Sharpe ratio portfolio.
        """
        if self.simulations_df is None:
            raise ValueError("Run the simulation first by calling run_simulation().")

        # Maximum Sharpe Ratio
        max_sharpe_ratio = self.simulations_df.loc[self.simulations_df['SharpeRatio'].idxmax()]
        portfolio_weight = max_sharpe_ratio['PortfolioWeights']
        mu = max_sharpe_ratio['Returns']
        ticker_weights_dict = dict(zip(self.tickers, portfolio_weight))
        return ticker_weights_dict, mu

    def get_min_volatility(self):
        """
        Retrieves the portfolio with the minimum Volatility from the simulations.
        Updates the provided allocations and expected returns dictionaries.

            """
        if self.simulations_df is None:
            raise ValueError("Run the simulation first by calling run_simulation().")

        # Minimum Volatility
        min_volatility = self.simulations_df.loc[self.simulations_df['Volatility'].idxmin()]
        portfolio_weight = min_volatility['PortfolioWeights']
        mu = min_volatility['Returns']
        ticker_weights_dict = dict(zip(self.tickers, portfolio_weight))
        return ticker_weights_dict, mu
