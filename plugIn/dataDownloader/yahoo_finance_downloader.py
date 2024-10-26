import yfinance as yf

import logging

from plugIn.dataDownloader.base_downloader import BaseDownloader

logger = logging.getLogger(__name__)


class YahooFinanceDownloader(BaseDownloader):
    def __init__(self, current_dir, asset_class):
        super().__init__(asset_class, current_dir)

    def download_data(self, tickers, start_date, end_date):
        sorted_tickers = sorted(list(tickers))
        logger.info(f"Downloading data for tickers: {sorted_tickers}")
        return yf.download(sorted_tickers, start=start_date, end=end_date)["Adj Close"]
