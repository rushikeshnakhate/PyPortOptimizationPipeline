import os
import unittest
import pandas as pd
import numpy as np

from src.common.conventions import PklFileConventions, HeaderConventions
from src.experimental.monte_carlo_simulation import MonteCarloSimulation, run_monte_carlo_simulation


class TestMonteCarloSimulation(unittest.TestCase):
    def setUp(self):
        # Create temporary directory for output
        self.test_output_dir = "test_output"
        os.makedirs(self.test_output_dir, exist_ok=True)

        # Generate synthetic data for testing
        np.random.seed(42)
        self.data = pd.DataFrame({
            "StockA": np.random.randn(100),
            "StockB": np.random.randn(100),
            "StockC": np.random.randn(100),
        })

    def tearDown(self):
        # Remove test output directory and files
        for file in os.listdir(self.test_output_dir):
            file_path = os.path.join(self.test_output_dir, file)
            os.remove(file_path)
        os.rmdir(self.test_output_dir)

    def test_simulation_run(self):
        # Test if the simulation runs and generates results
        simulation = MonteCarloSimulation(self.data, self.test_output_dir, num_of_portfolios=1000)
        simulation.run_simulation(rerun=True)
        self.assertIsNotNone(simulation.simulations_df)
        self.assertTrue(os.path.exists(simulation.pkl_filepath))
        self.assertGreater(len(simulation.simulations_df), 0)

    def test_max_sharpe_ratio(self):
        # Test retrieving the max Sharpe ratio portfolio
        simulation = MonteCarloSimulation(self.data, self.test_output_dir, num_of_portfolios=1000)
        simulation.run_simulation(rerun=True)
        max_sharpe_portfolio = simulation.get_max_sharpe_ratio()
        self.assertIn(HeaderConventions.sharpe_ratio_column, max_sharpe_portfolio.columns)
        self.assertEqual(len(max_sharpe_portfolio), 1)

    def test_min_volatility(self):
        # Test retrieving the min volatility portfolio
        simulation = MonteCarloSimulation(self.data, self.test_output_dir, num_of_portfolios=1000)
        simulation.run_simulation(rerun=True)
        min_volatility_portfolio = simulation.get_min_volatility()
        self.assertIn(HeaderConventions.annual_volatility_column, min_volatility_portfolio.columns)
        self.assertEqual(len(min_volatility_portfolio), 1)

    def test_run_monte_carlo_simulation(self):
        # Test the main Monte Carlo simulation function
        result_df = run_monte_carlo_simulation(self.test_output_dir, self.data)
        self.assertIsNotNone(result_df)
        self.assertTrue(len(result_df) > 0)
        self.assertTrue(os.path.exists(
            os.path.join(self.test_output_dir, PklFileConventions.short_listed_monte_carlo_pkl_filename)))


if __name__ == "__main__":
    unittest.main()
