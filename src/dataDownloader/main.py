import os

import pandas as pd

from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.common.hydra_config_loader import load_config

from src.dataDownloader.alpha_vantage_downloader import AlphaVantageDownloader
from src.dataDownloader.bonds import Bonds
from src.dataDownloader.conventions import SourceTypeConventions, AssetTypeConventions
from src.dataDownloader.custom_csv_downloader import CustomCSVDownloader
from src.dataDownloader.stocks import Stocks
from src.dataDownloader.yahoo_finance_downloader import YahooFinanceDownloader


@ExecutionTimeRecorder(module_name=__name__)
def get_downloader(source_type, current_dir, asset_class, **kwargs):
    if source_type == SourceTypeConventions.YahooFinance:
        return YahooFinanceDownloader(current_dir, asset_class)
    elif source_type == SourceTypeConventions.AlphaVantage:
        return AlphaVantageDownloader(current_dir, api_key=kwargs.get('api_key'))
    elif source_type == SourceTypeConventions.CustomCSV:
        return CustomCSVDownloader(current_dir, file_path=kwargs.get('file_path'))
    else:
        raise ValueError(f"Unknown data source: {source_type}")


@ExecutionTimeRecorder(module_name=__name__)
def get_asset(asset_type, start_date, end_date, data_source, **kwargs):
    if asset_type == AssetTypeConventions.stocks:
        return Stocks(start_date, end_date, data_source, **kwargs)
    elif asset_type == AssetTypeConventions.bonds:
        return Bonds(start_date, end_date, data_source, **kwargs)
    # elif asset_type == "commodities":
    #     return Commodities(start_date, end_date, data_source, **kwargs)
    else:
        raise ValueError("Unknown asset type")


@ExecutionTimeRecorder(module_name=__name__)  # Decorate the function
def get_data(current_dir, start_date, end_date,
             tickers=None,
             api_key=None,
             file_path=None,
             source_type="YahooFinance",
             asset_type="stocks"):
    """
    Fetch data for specified tickers or configurations.

    Parameters:
        current_dir (str): Current directory for saving/loading data.
        start_date (str): Start date for data fetching (YYYY-MM-DD).
        end_date (str): End date for data fetching (YYYY-MM-DD).
        api_key (str, optional): API key for data source (if required).
        file_path (str, optional): File path for CSV source (if applicable).
        tickers (list, optional): List of tickers to fetch data for.
                                  If provided, configuration sources are ignored.

    Returns:
        pd.DataFrame: Combined data for the specified tickers.
        :param file_path:
        :param api_key:
        :param end_date:
        :param start_date:
        :param current_dir:
        :param tickers:
        :param asset_type:
        :param source_type:
    """
    # Determine the module name for configuration
    module_name = os.path.basename(os.path.dirname(__file__))

    # If tickers are provided, use them directly instead of configuration
    if tickers:
        # Create a generic source configuration for passed tickers

        data_source = get_downloader(
            source_type=source_type,
            current_dir=current_dir,
            asset_class=asset_type,
            api_key=api_key,
            file_path=file_path,
        )

        asset_factory = get_asset(
            asset_type=asset_type,
            start_date=start_date,
            end_date=end_date,
            data_source=data_source,
        )

        # Fetch data for the provided tickers
        data = asset_factory.fetch_data(tickers)
        return data

    # If no tickers are passed, use configuration to fetch data
    configuration = load_config(module_name)
    all_data = []

    for source_cfg in configuration.sources:
        source_type = source_cfg.source_type
        asset_type = source_cfg.asset_class

        data_source = get_downloader(
            source_type=source_type,
            current_dir=current_dir,
            asset_class=asset_type,
            api_key=api_key,
            file_path=file_path,
        )

        asset_factory = get_asset(
            asset_type=asset_type,
            start_date=start_date,
            end_date=end_date,
            data_source=data_source,
        )

        # Fetch data based on tickers in configuration
        data = asset_factory.fetch_data(source_cfg.tickers)
        all_data.append(data)

    # Concatenate or merge all data
    combined_data = pd.concat(all_data, axis=1)  # Adjust concatenation based on requirements
    return combined_data
