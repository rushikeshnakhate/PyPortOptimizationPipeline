import os
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm


# Monte Carlo Simulation Class
class MonteCarloSimulation:
    def __init__(self, data, num_of_portfolios=5):
        self.tickers = data.columns
        self.data = data
        self.num_of_portfolios = num_of_portfolios
        self.log_return = np.log(1 + data.pct_change())
        self.number_of_symbols = len(self.tickers)
        self.simulations_df = None

    def run_simulation(self, rerun=False):
        """
        Runs the Monte Carlo simulation to generate portfolio weights,
        returns, volatilities, and Sharpe ratios.
        """
        output_dir = Path(r"D:\PortOpt\data")
        pkl_filepath = os.path.join(output_dir, "simulation.pkl")

        # Check if rerun is required or simulation pickle file exists
        if not rerun and os.path.exists(pkl_filepath):
            self.simulations_df = pd.read_pickle(pkl_filepath)
        else:
            self._run_simulation_now()
            self.simulations_df.to_pickle(pkl_filepath)

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
            'Expected Annual Return': ret_arr,
            'Annual Volatility': vol_arr,
            'Sharpe Ratio': sharpe_arr
        })
        self.simulations_df['Weights'] = weights_dicts

    def _get_portfolio_by(self, criterion='Sharpe Ratio', maximize=True):
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
        selected_portfolio['Expected Return Type'] = title
        selected_portfolio['Risk Model'] = title
        selected_portfolio['Optimizer'] = title
        return pd.DataFrame(selected_portfolio).T

    def get_max_sharpe_ratio(self):
        """Retrieve the portfolio with the maximum Sharpe ratio."""
        return self._get_portfolio_by(criterion='Sharpe Ratio', maximize=True)

    def get_min_volatility(self):
        """Retrieve the portfolio with the minimum volatility."""
        return self._get_portfolio_by(criterion='Annual Volatility', maximize=False)

    def run_monte_carlo_simulation(self):
        """Run the Monte Carlo Simulation and return max Sharpe ratio and min volatility portfolios."""
        self.run_simulation()
        return self.get_max_sharpe_ratio(), self.get_min_volatility()

#
# if __name__ == "__main__":
#     data = get_stocks()
#     monteCarloSimulation = MonteCarloSimulation(data)
#     max_sharpe_ratio, min_volatility = monteCarloSimulation.run_monte_carlo_simulation()
#     print(tabulate(max_sharpe_ratio, headers='keys', tablefmt='grid'))
#     print(tabulate(min_volatility, headers='keys', tablefmt='grid'))
