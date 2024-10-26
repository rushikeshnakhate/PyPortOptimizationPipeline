import pandas as pd

import logging

from plugIn.dataDownloader.base_downloader import BaseDownloader

logger = logging.getLogger(__name__)


class CustomCSVDownloader(BaseDownloader):
    def __init__(self, current_dir, file_path):
        super().__init__('stocks', current_dir)
        self.file_path = file_path

    def download_data(self, tickers, start_date, end_date):
        logger.info(f"Loading data from CSV at {self.file_path}")
        df = pd.read_csv(self.file_path, parse_dates=True, index_col='Date')
        return df.loc[start_date:end_date, tickers]
