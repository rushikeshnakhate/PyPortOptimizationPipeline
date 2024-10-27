import os

import pandas as pd
from alpha_vantage.commodities import Commodities

from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.common.hydra_config_loader import load_config

from plugIn.dataDownloader.alpha_vantage_downloader import AlphaVantageDownloader
from plugIn.dataDownloader.bonds import Bonds
from plugIn.dataDownloader.custom_csv_downloader import CustomCSVDownloader
from plugIn.dataDownloader.stocks import Stocks
from plugIn.dataDownloader.yahoo_finance_downloader import YahooFinanceDownloader


@ExecutionTimeRecorder(module_name=__name__)
def get_downloader(source_type, current_dir, asset_class, **kwargs):
    if source_type == 'YahooFinance':
        return YahooFinanceDownloader(current_dir, asset_class)
    elif source_type == 'AlphaVantage':
        return AlphaVantageDownloader(current_dir, api_key=kwargs.get('api_key'))
    elif source_type == 'CustomCSV':
        return CustomCSVDownloader(current_dir, file_path=kwargs.get('file_path'))
    else:
        raise ValueError(f"Unknown data source: {source_type}")


@ExecutionTimeRecorder(module_name=__name__)
def get_asset(asset_type, start_date, end_date, data_source, **kwargs):
    if asset_type == "stocks":
        return Stocks(start_date, end_date, data_source, **kwargs)
    elif asset_type == "bonds":
        return Bonds(start_date, end_date, data_source, **kwargs)
    elif asset_type == "commodities":
        return Commodities(start_date, end_date, data_source, **kwargs)
    else:
        raise ValueError("Unknown asset type")


@ExecutionTimeRecorder(module_name=__name__)  # Decorate the function
def get_data(current_dir, start_date, end_date, api_key=None, file_path=None):
    module_name = os.path.basename(os.path.dirname(__file__))
    configuration = load_config(module_name)
    all_data = []
    for source_cfg in configuration.sources:
        source_type = source_cfg.source_type
        asset_type = source_cfg.asset_class

        data_source = get_downloader(source_type=source_type,
                                     current_dir=current_dir,
                                     asset_class=asset_type,
                                     api_key=api_key,
                                     file_path=file_path)
        asset_factory = get_asset(asset_type=asset_type,
                                  start_date=start_date,
                                  end_date=end_date,
                                  data_source=data_source)
        data = asset_factory.fetch_data(source_cfg.tickers)
        all_data.append(data)
        # Concatenate or merge all data
    combined_data = pd.concat(all_data, axis=1)  # Adjust concatenation based on requirements
    return combined_data
