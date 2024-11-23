import os
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import pandas as pd

from src.performance_metrics.main import calculate_performance


class TestCalculatePerformance(unittest.TestCase):

    @patch('src.common.utils.load_data_from_pickle')
    @patch('src.common.utils.save_data_to_pickle')
    @patch('src.performance_metrics.portfolio_return.PortfolioReturn')
    @patch('src.performance_metrics.portfolio_sharpratio.PortfolioSharpeRatio')
    @patch('src.performance_metrics.portfolio_volatility.PortfolioVolatility')
    @patch('src.performance_metrics.portfoliio_performance.PortfolioWithAllocatedWeights')
    @patch('src.performance_metrics.performance_metrics_name_convernsions.PerformanceMetricsNameConventions')
    @patch('src.common.conventions.PklFileConventions')
    @patch('logging.getLogger')
    def test_calculate_performance(self, mock_logger, mock_PklFileConventions, mock_PerformanceMetricsNameConventions,
                                   mock_PortfolioWithAllocatedWeights, mock_PortfolioVolatility,
                                   mock_PortfolioSharpeRatio,
                                   mock_PortfolioReturn, mock_save_data, mock_load_data):
        # Set up the mocks
        mock_logger.return_value = MagicMock()
        mock_PklFileConventions.performance_pkl_filename = 'performance.pkl'

        mock_load_data.return_value = pd.DataFrame({
            'Allocation_Greedy': ["{'asset_1': 0.4, 'asset_2': 0.6}", "{'asset_1': 0.5, 'asset_2': 0.5}"],
            'Allocation_LP': ["{'asset_1': 0.3, 'asset_2': 0.7}", "{'asset_1': 0.6, 'asset_2': 0.4}"],
            'Greedy_remaining_amount': [1000, 1500],
            'LP_remaining_amount': [2000, 2500]
        })

        mock_PortfolioWithAllocatedWeights.return_value = MagicMock()
        mock_PortfolioVolatility.return_value.calculate.return_value = 0.12  # Mocked volatility value
        mock_PortfolioReturn.return_value.calculate.return_value = 0.05  # Mocked return value
        mock_PortfolioSharpeRatio.return_value.calculate.return_value = 1.2  # Mocked Sharpe ratio value

        # Example input
        post_processing_df = pd.DataFrame({
            'Allocation_Greedy': ["{'asset_1': 0.4, 'asset_2': 0.6}", "{'asset_1': 0.5, 'asset_2': 0.5}"],
            'Allocation_LP': ["{'asset_1': 0.3, 'asset_2': 0.7}", "{'asset_1': 0.6, 'asset_2': 0.4}"],
            'Greedy_remaining_amount': [1000, 1500],
            'LP_remaining_amount': [2000, 2500]
        })

        data = {
            'asset_1': [100, 105, 110, 108, 107],
            'asset_2': [200, 195, 193, 191, 190]
        }

        start_date = "2024-01-01"
        end_date = "2024-01-31"
        current_month_dir = Path(os.getcwd())

        # Call the function being tested
        result_df = calculate_performance(post_processing_df, data, start_date, end_date, current_month_dir)

        # Assertions
        # Check that the performance metrics were added to the DataFrame
        self.assertIn('Allocation_Greedy', result_df.columns)
        self.assertIn('Allocation_LP', result_df.columns)
        self.assertIn('Greedy_remaining_amount', result_df.columns)
        self.assertIn('LP_remaining_amount', result_df.columns)


if __name__ == '__main__':
    unittest.main()
