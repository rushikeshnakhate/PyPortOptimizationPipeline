# Subclass for stock data from Yahoo Finance
import logging
import os

from statsmodels.sandbox.tsa.try_var_convolve import yf

from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.common.hydra_config_loader import load_config
from plugIn.dataDownloader.base_data_downloader import BaseDataDownloader

logger = logging.getLogger(__name__)


class StockDataDownloader(BaseDataDownloader):
    def __init__(self, start_date, end_date, current_dir):
        super().__init__('stocks', start_date, end_date, current_dir)

    @ExecutionTimeRecorder(module_name='download_stocks')  # Decorate function
    def download_data(self):
        """Downloads stock data from Yahoo Finance."""
        module_name = os.path.basename(os.path.dirname(__file__))
        stocks_config = load_config(module_name)
        tickers = stocks_config.tickers
        sorted_tickers = sorted(list(tickers))
        logger.info(f"Tickers list: {sorted_tickers}")
        data = yf.download(sorted_tickers, start=self.start_date, end=self.end_date)["Adj Close"]
        return data
