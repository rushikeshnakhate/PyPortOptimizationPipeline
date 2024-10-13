import logging
import os

import pandas as pd
import yfinance as yf

from plugIn.common.conventions import PklFileConventions
from plugIn.common.utils import load_config

logger = logging.getLogger(__name__)


# write a function to check if the pickle file exists
# if it does, load the data from the pickle file
# if it doesn't, download the data from yfinance
# and save the data to a pickle file
# return the data
def get_stocks(start_date, end_date, current_dir):
    logger.info(f"getting stocks start_date={start_date}, end_date={end_date}")
    try:
        pkl_filepath = os.path.join(current_dir, PklFileConventions.data_pkl_filename)
        if not os.path.exists(pkl_filepath):
            logging.info(
                f"Downloading stock data from yfinance for {start_date} to {end_date} and saving to {pkl_filepath}")
            df = download_stock_data(start_date, end_date)
            df.to_pickle(pkl_filepath)
        else:
            logger.info(f"Loading stock data from {pkl_filepath}")
            df = pd.read_pickle(pkl_filepath)
        return df
    except Exception as ex:
        raise ValueError(f"error in getting stocks..{ex}")


def download_stock_data(start_date, end_date):
    module_name = os.path.basename(os.path.dirname(__file__))
    returns_cfg = load_config(module_name)
    tickers = returns_cfg.expected_returns.enabled_methods
    tickers.sort()
    data = yf.download(tickers, start=start_date, end=end_date)["Adj Close"]
    return data
