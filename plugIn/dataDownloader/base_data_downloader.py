import logging
import os
from abc import ABC, abstractmethod

import pandas as pd

from plugIn.common.conventions import PklFileConventions

logger = logging.getLogger(__name__)


# Base class for asset data download
class BaseDataDownloader(ABC):
    def __init__(self, asset_class, start_date, end_date, current_dir):
        self.asset_class = asset_class
        self.start_date = start_date
        self.end_date = end_date
        self.current_dir = current_dir

    @abstractmethod
    def download_data(self):
        """Method to be implemented by subclasses for downloading data."""
        pass

    def get_data(self):
        """Generic method for loading and caching asset data."""
        logger.info(
            f"Getting data for asset_class={self.asset_class}, start_date={self.start_date}, end_date={self.end_date}")
        try:
            pkl_filepath = os.path.join(self.current_dir, PklFileConventions.data_pkl_filename)
            if not os.path.exists(pkl_filepath):
                logger.info(
                    f"Downloading data for {self.asset_class} from {self.start_date} to {self.end_date} and saving to {pkl_filepath}")
                df = self.download_data()
                df.to_pickle(pkl_filepath)
            else:
                logger.info(f"Loading cached data from {pkl_filepath}")
                df = pd.read_pickle(pkl_filepath)
            return df
        except Exception as ex:
            raise ValueError(f"Error in getting data for {self.asset_class}: {ex}")
