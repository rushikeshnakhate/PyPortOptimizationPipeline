import logging
import os

import pandas as pd
import yfinance as yf

from src.common.conventions import PklFileConventions
from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.common.hydra_config_loader import load_config

logger = logging.getLogger(__name__)

logging.getLogger("yfinance").setLevel(logging.WARNING)
logging.getLogger("yfinance").setLevel(logging.WARNING)
logging.getLogger("peewee").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


@ExecutionTimeRecorder(module_name=__name__)  # Decor
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


@ExecutionTimeRecorder(module_name=__name__)  # Decorate the function
def download_stock_data(start_date, end_date):
    module_name = os.path.basename(os.path.dirname(__file__))
    stocks = load_config(module_name)
    tickers = stocks.tickers
    sorted_tickers = sorted(list(tickers))
    logger.info(f"tickers list:{sorted_tickers}")
    data = yf.download(sorted_tickers, start=start_date, end=end_date)["Close"]
    return data
