import logging
import os

import pandas as pd

from plugIn.common.conventions import PklFileConventions
from plugIn.common.hydra_config_loader import HydraConfigLoader
from plugIn.common.utils import load_config
from plugIn.expected_return.arithmetic_mean_historical_return import ArithmeticMeanHistoricalReturn
from plugIn.expected_return.black_litterman import BlackLittermanReturn
from plugIn.expected_return.cagr_mean_historical_return import CAGRMeanHistoricalReturn
from plugIn.expected_return.capm_return import CAPMReturn
from plugIn.expected_return.ema_historical_return import EMAHistoricalReturn
from plugIn.expected_return.fama_french import FamaFrenchReturn
from plugIn.expected_return.gordon_growth import GordonGrowthReturn
from plugIn.expected_return.holt_winters import HoltWintersReturn
from plugIn.expected_return.machine_learning_arima import ARIMAReturn
from plugIn.expected_return.machine_learning_linearRegression import LinearRegressionReturn
from plugIn.expected_return.risk_parity import RiskParityReturn
from plugIn.expected_return.twrr_return import TWRRReturn

logger = logging.getLogger(__name__)


def update_returns_dataframe(df_returns, return_type, return_values):
    return_series = pd.Series(return_values, name=return_type)
    return df_returns.join(return_series, how='outer')


def calculate_all_returns(data, output_dir):
    """Calculate all the different returns (mean, ema, capm, etc.) using a loop."""
    # Create a mapping of return types to their respective classes
    module_name = os.path.basename(os.path.dirname(__file__))
    returns_cfg = load_config(module_name)
    enabled_methods = returns_cfg.expected_returns.enabled_methods

    return_calculators = {
        'CAGRMeanHistorical': CAGRMeanHistoricalReturn(data),
        'ArithmeticMeanHistorical': ArithmeticMeanHistoricalReturn(data),
        'EMAHistorical': EMAHistoricalReturn(data),
        'CAPM': CAPMReturn(data),
        'GordonGrowth': GordonGrowthReturn(data),
        'FamaFrench': FamaFrenchReturn(data),
        'LinearRegression': LinearRegressionReturn(data),
        'RiskParity': RiskParityReturn(data),
        'BlackLitterman': BlackLittermanReturn(data),
        'ARIMA': ARIMAReturn(data),
        'TWRR': TWRRReturn(data),
        'HoltWinters': HoltWintersReturn(data),
    }

    # Initialize an empty DataFrame to store returns
    df_returns = pd.DataFrame()

    # Loop through each return type and add to the DataFrame
    for return_type in enabled_methods:
        if return_type in return_calculators:
            logger.debug("Calculating expected return for: %s", return_type)
            calculator = return_calculators[return_type]
            return_values = calculator.calculate_expected_return()
            logger.debug("Return values for %s: %s", return_type, return_values)
            df_returns = update_returns_dataframe(df_returns, return_type, return_values)
        else:
            logger.warning("Return type %s not found in return calculators", return_type)
    df_returns.to_pickle(output_dir / PklFileConventions.expected_return_pkl_filename)
    return df_returns


def calculate_or_get_all_return(data, current_month_dir):
    logger.info("Calculating or getting all returns...for the month {}".format(current_month_dir))
    expected_return_pkl_filepath = current_month_dir / PklFileConventions.expected_return_pkl_filename
    if expected_return_pkl_filepath.exists():
        return pd.read_pickle(expected_return_pkl_filepath)
    return calculate_all_returns(data, current_month_dir)

#
# if __name__ == "__main__":
#     output_dir = Path(r"D:\PortfoliOpt\data")
#     year = 2023
#     month_ranges = generate_month_date_ranges(year, months=[1])
#     for start_date, end_date in month_ranges:
#         current_month_dir = create_current_month_directory(start_date, output_dir)
#         data = get_stocks(start_date, end_date, current_month_dir)
#         expected_return_df = calculate_all_returns(data, current_month_dir)
#         print(tabulate(expected_return_df, headers='keys', tablefmt='grid'))
