import logging
import os
from pathlib import Path

import pandas as pd

from src.common.conventions import PklFileConventions
from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.common.hydra_config_loader import load_config
from src.expected_return.arithmetic_mean_historical_return import ArithmeticMeanHistoricalReturn
from src.expected_return.black_litterman import BlackLittermanReturn
from src.expected_return.cagr_mean_historical_return import CAGRMeanHistoricalReturn
from src.expected_return.capm_return import CAPMReturn
from src.expected_return.ema_historical_return import EMAHistoricalReturn
from src.expected_return.fama_french import FamaFrenchReturn
from src.expected_return.gordon_growth import GordonGrowthReturn
from src.expected_return.holt_winters import HoltWintersReturn
from src.expected_return.machine_learning_arima import ARIMAReturn
from src.expected_return.machine_learning_linearRegression import LinearRegressionReturn
from src.expected_return.risk_parity import RiskParityReturn
from src.expected_return.twrr_return import TWRRReturn

logger = logging.getLogger(__name__)


def update_returns_dataframe(df_returns, return_type, return_values):
    # Ensure return_values DataFrame has 'Ticker' as the index
    return_values.set_index('Ticker', inplace=True)
    # Rename the column to include the return type (e.g., "ExpectedReturn_ARIMA")
    return_values.columns = [f'ExpectedReturn_{return_type}']
    # Join on 'Ticker' index
    df_returns = df_returns.join(return_values, how='outer')
    return df_returns


@ExecutionTimeRecorder(module_name=__name__)  # Use __name__ t
def calculate_all_returns(data, output_dir, enabled_methods):
    """Calculate all the different returns (mean, ema, capm, etc.) using a loop."""
    # Create a mapping of return types to their respective classes
    return_calculators = get_expected_return_enabled_classes(data)
    # Initialize an empty DataFrame to store returns
    df_returns = pd.DataFrame()
    # Loop through each return type and add to the DataFrame
    for enabled_method in enabled_methods:
        if enabled_method in return_calculators:
            logger.debug("Calculating expected return for: %s", enabled_method)
            calculator = return_calculators[enabled_method]
            return_values = calculator.calculate_expected_return(output_dir)
            df_returns = pd.concat([df_returns, return_values], axis=1)
        else:
            logger.warning("Return type %s not found in return calculators", enabled_method)
    df_returns.to_pickle(output_dir / PklFileConventions.expected_return_for_all_type_pkl_filename)
    return df_returns


def get_expected_return_enabled_classes(data):
    return_calculators = {
        'ARIMA': ARIMAReturn(data),
        'ArithmeticMeanHistorical': ArithmeticMeanHistoricalReturn(data),
        'BlackLitterman': BlackLittermanReturn(data),
        'CAPM': CAPMReturn(data),
        'CAGRMeanHistorical': CAGRMeanHistoricalReturn(data),
        'EMAHistorical': EMAHistoricalReturn(data),
        'FamaFrench': FamaFrenchReturn(data),
        'GordonGrowth': GordonGrowthReturn(data),
        'HoltWinters': HoltWintersReturn(data),
        'LinearRegression': LinearRegressionReturn(data),
        'RiskParity': RiskParityReturn(data),
        'TWRR': TWRRReturn(data)
    }
    return return_calculators


def get_enabled_methods():
    module_name = os.path.basename(os.path.dirname(__file__))
    returns_cfg = load_config(module_name)
    enabled_methods = returns_cfg.expected_returns.enabled_methods
    logger.info("loading config for enabled_methods: %s", enabled_methods)
    return enabled_methods


@ExecutionTimeRecorder(module_name=__name__)  # Use __name__ t
def calculate_or_get_all_return(data: pd.DataFrame, current_dir: Path, enabled_methods=None):
    logger.info("Calculating or getting all returns...for the month {}".format(current_dir))
    if enabled_methods is None:
        # If enabled_methods is not provided, load it from the config file
        enabled_methods = get_enabled_methods()
    return calculate_all_returns(data, current_dir, enabled_methods)
