import os
import unittest
from unittest.mock import patch, MagicMock

import pandas as pd

from src.dataDownloader.main import get_data


class TestGetData(unittest.TestCase):

    def test_get_data_with_tickers(self):
        current_dir = os.getcwd()
        tickers = ["AAPL", "GOOGL"]
        result = get_data(
            tickers=tickers,
            current_dir=current_dir,
            start_date="2024-01-01",
            end_date="2024-01-31"
        )
        df = pd.read_pickle("stocks.pkl")

        # Check if the tickers are in the DataFrame's columns
        for ticker in tickers:
            self.assertIn(ticker, df.columns, f"{ticker} not found in the DataFrame")

        # Optionally check if the data is not empty (e.g., first row check)
        self.assertFalse(df.empty, "DataFrame is empty")
        # For now, if you want to simulate file cleanup after data is downloaded, use:
        temp_files = [f for f in os.listdir(current_dir) if f.endswith("pkl")]
        for file in temp_files:
            file_path = os.path.join(current_dir, file)
            os.remove(file_path)
