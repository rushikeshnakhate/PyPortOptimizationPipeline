# from alpha_vantage.timeseries import TimeSeries
import pandas as pd

import logging

from src.dataDownloader.base_downloader import BaseDownloader

logger = logging.getLogger(__name__)


class AlphaVantageDownloader(BaseDownloader):
    def __init__(self, current_dir, api_key):
        super().__init__('stocks', current_dir)
        self.api_key = api_key

    def download_data(self, tickers, start_date, end_date):
        pass
        # ts = TimeSeries(key=self.api_key, output_format='pandas')
        # data = pd.DataFrame()
        # for ticker in tickers:
        #     logger.info(f"Fetching data for {ticker} from Alpha Vantage")
        #     data[ticker], _ = ts.get_daily_adjusted(symbol=ticker, outputsize='full')
        # return data.loc[start_date:end_date]
