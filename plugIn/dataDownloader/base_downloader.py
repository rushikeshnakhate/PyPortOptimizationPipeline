import os
import pandas as pd
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseDownloader(ABC):
    def __init__(self, asset_class, current_dir):
        self.asset_class = asset_class
        self.current_dir = current_dir

    def get_data(self, tickers, start_date, end_date):
        pkl_filepath = os.path.join(self.current_dir, f"{self.asset_class}_{start_date}_{end_date}.pkl")
        if os.path.exists(pkl_filepath):
            logger.info(f"Loading cached data from {pkl_filepath}")
            return pd.read_pickle(pkl_filepath)
        else:
            logger.info(f"Downloading data for {self.asset_class} and saving to {pkl_filepath}")
            df = self.download_data(tickers, start_date, end_date)
            df.to_pickle(pkl_filepath)
            return df

    @abstractmethod
    def download_data(self, tickers, start_date, end_date):
        """Method to be implemented by subclasses for downloading data."""
        pass
