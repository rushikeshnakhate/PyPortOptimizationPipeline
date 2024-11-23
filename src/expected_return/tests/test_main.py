import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
from pathlib import Path
from src.expected_return.arithmetic_mean_historical_return import ArithmeticMeanHistoricalReturn
from src.expected_return.black_litterman import BlackLittermanReturn
from src.expected_return.machine_learning_arima import ARIMAReturn
from src.common.conventions import PklFileConventions
from src.main import calculate_or_get_all_return  # assuming the function is in main.py


class TestCalculateReturns(unittest.TestCase):

    @patch('src.main.load_config')  # Mocking load_config to control enabled_methods
    @patch.object(ArithmeticMeanHistoricalReturn,
                  'calculate_expected_return')  # Mocking method of the return calculators
    @patch.object(BlackLittermanReturn, 'calculate_expected_return')  # Mocking method of the return calculators
    @patch.object(ARIMAReturn, 'calculate_expected_return')  # Mocking method of the return calculators
    def test_calculate_or_get_all_return(self, mock_arima, mock_black_litterman, mock_arithmetic_mean,
                                         mock_load_config):
        # Sample test data (with Ticker as the index)
        data = pd.DataFrame({
            'AAPL': [184.73, 183.35, 181.02, 180.29, 184.65, 184.24],
            'GOOGL': [137.82, 138.57, 136.05, 135.39, 138.50, 140.60]
        }, index=pd.to_datetime([
            '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-08', '2024-01-09'
        ]))

        # Set up the mock return values for the expected return calculations
        mock_arithmetic_mean.return_value = pd.DataFrame({
            'Ticker': ['AAPL', 'GOOGL'],
            'ExpectedReturn_ArithmeticMeanHistorical': [0.05, 0.04]
        }).set_index('Ticker')

        mock_black_litterman.return_value = pd.DataFrame({
            'Ticker': ['AAPL', 'GOOGL'],
            'ExpectedReturn_BlackLitterman': [0.03, 0.02]
        }).set_index('Ticker')

        mock_arima.return_value = pd.DataFrame({
            'Ticker': ['AAPL', 'GOOGL'],
            'ExpectedReturn_ARIMA': [0.06, 0.05]
        }).set_index('Ticker')

        # Define enabled methods manually for this test case
        enabled_methods = ['ArithmeticMeanHistorical', 'BlackLitterman', 'ARIMA']

        # Mock the config file loading behavior
        mock_load_config.return_value = MagicMock(expected_returns=MagicMock(enabled_methods=enabled_methods))

        # Path for saving the .pkl file
        test_output_dir = Path('./test_output')
        test_output_dir.mkdir(parents=True, exist_ok=True)

        # Run the function
        result_df = calculate_or_get_all_return(data, test_output_dir, enabled_methods=enabled_methods)

        # Check if the returned DataFrame has the expected columns
        self.assertTrue('ExpectedReturn_ArithmeticMeanHistorical' in result_df.columns)
        self.assertTrue('ExpectedReturn_BlackLitterman' in result_df.columns)
        self.assertTrue('ExpectedReturn_ARIMA' in result_df.columns)

        # Verify that the .pkl file is created
        pkl_path = test_output_dir / PklFileConventions.expected_return_for_all_type_pkl_filename
        self.assertTrue(pkl_path.exists())

        # Clean up: remove the .pkl file after the test
        os.remove(pkl_path)

    def tearDown(self):
        """Clean up any files created during the tests"""
        test_output_dir = Path('./test_output')
        if test_output_dir.exists():
            for file in test_output_dir.iterdir():
                if file.suffix == '.pkl':
                    os.remove(file)
            test_output_dir.rmdir()  # Remove the test output directory if empty


if __name__ == '__main__':
    unittest.main()
