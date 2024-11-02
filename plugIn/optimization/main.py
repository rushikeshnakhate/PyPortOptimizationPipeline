import logging
import os

import numpy as np
import pandas as pd

from plugIn.common.conventions import HeaderConventions
from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.common.hydra_config_loader import load_config
from plugIn.optimization.add_risk_folio_optimizer import ADDRiskFolioOptimizer
from plugIn.optimization.cadr_risk_folio_optimizer import CDaRRiskFolioOptimizer
from plugIn.optimization.cvarr_risk_folio_optimizer import CVaRRiskFolioOptimizer
from plugIn.optimization.eadr_risk_folio_optimizer import EDaRRiskFolioOptimizer
from plugIn.optimization.evarr_risk_folio_optimizer import EVaRRiskFolioOptimizer
from plugIn.optimization.flpm_v_risk_folio_optimizer import FLPMRiskFolioOptimizer
from plugIn.optimization.frontier_with_short_position import PyPortfolioOptFrontierWithShortPosition
from plugIn.optimization.mad_risk_folio_optimizer import MADRiskFolioOptimizer
from plugIn.optimization.mdd_risk_folio_optimizer import MDDRiskFolioOptimizer
from plugIn.optimization.msv_risk_folio_optimizer import MSVRiskFolioOptimizer
from plugIn.optimization.mv_risk_folio_optimizer import MVRiskFolioOptimizer
from plugIn.optimization.py_portfolio_opt_frontier import PyPortfolioOptFrontier
from plugIn.optimization.slpm_risk_folio_optimizer import SLPMRiskFolioOptimizer
from plugIn.optimization.uci_risk_folio_optimizer import UCIRiskFolioOptimizer
from plugIn.optimization.wr_risk_folio_optimizer import WRRiskFolioOptimizer

logger = logging.getLogger(__name__)


def get_all_efficient_frontier_optimizer(expected_return_type,
                                         risk_model_name,
                                         expected_returns,
                                         covariance_matrix,
                                         current_month_dir,
                                         enabled_methods,
                                         data=None):
    optimizers = {
        'pyPortfolioOptFrontier': PyPortfolioOptFrontier,
        'pyPortfolioOptFrontierWithShortPosition': PyPortfolioOptFrontierWithShortPosition,
        'MVRiskFolioOptimizer': MVRiskFolioOptimizer,
        'MADRiskFolioOptimizer': MADRiskFolioOptimizer,
        'MSVRiskFolioOptimizer': MSVRiskFolioOptimizer,
        'FLPMRiskFolioOptimizer': FLPMRiskFolioOptimizer,
        'SLPMRiskFolioOptimizer': SLPMRiskFolioOptimizer,
        'CVaRRiskFolioOptimizer': CVaRRiskFolioOptimizer,
        'EVaRRiskFolioOptimizer': EVaRRiskFolioOptimizer,
        'WRRiskFolioOptimizer': WRRiskFolioOptimizer,
        'MDDRiskFolioOptimizer': MDDRiskFolioOptimizer,
        'ADDRiskFolioOptimizer': ADDRiskFolioOptimizer,
        'CDaRRiskFolioOptimizer': CDaRRiskFolioOptimizer,
        'UCIRiskFolioOptimizer': UCIRiskFolioOptimizer,
        'EDaRRiskFolioOptimizer': EDaRRiskFolioOptimizer
    }

    # Dictionary to store covariance matrices for each risk model
    optimizers_dict = {}

    for enabled_method in enabled_methods:
        if enabled_method in optimizers:
            optimizer = optimizers[enabled_method]
            try:
                logger.info(
                    f"Calculating efficient frontier for current_date=`{current_month_dir}`,Risk Model=`{risk_model_name}`, "
                    f"Return Type=`{expected_return_type}`" + f",optimizer=`{optimizer}`")

                optimizer_instance = optimizer(expected_returns=expected_returns,
                                               covariance_matrix=covariance_matrix,
                                               expected_return_type=expected_return_type,
                                               risk_return_type=risk_model_name,
                                               output_dir=current_month_dir,
                                               data=data)
                optimizer_instance.calculate_efficient_frontier()
                optimizer_results = optimizer_instance.get_results()
                optimizers_dict[optimizer] = optimizer_results
            except Exception as e:
                logger.error(
                    f"Calculating efficient frontier current_date=`{current_month_dir},Risk Model=`{risk_model_name}`, "
                    f"Return Type=`{expected_return_type}`" + f",optimizer=`{optimizer}`" + f" failed with error: {e}")
                optimizers_dict[optimizer] = f" failed with error: {e}"
        else:
            logger.warning("Optimizer{}  %s not found in return optimizers_dict={}", enabled_method, optimizers_dict)
    return optimizers_dict


def process_optimizer_results(expected_return_type, risk_model_name, mu, cov_matrix, data, current_month_dir,
                              enabled_methods):
    """
    Process the optimizer results for a given return type and risk model.
    """
    results = []
    try:
        optimizers_dict = get_all_efficient_frontier_optimizer(expected_return_type,
                                                               risk_model_name,
                                                               mu,
                                                               cov_matrix,
                                                               current_month_dir,
                                                               enabled_methods,
                                                               data)
        for optimizer_name, result in optimizers_dict.items():
            error_rows = result[HeaderConventions.cleaned_weights_column].astype(str).str.contains("error", case=False,
                                                                                                   na=False)
            if error_rows.any():
                result_dict = {
                    HeaderConventions.expected_return_column: expected_return_type,
                    HeaderConventions.risk_model_column: risk_model_name,
                    HeaderConventions.optimizer_column: optimizer_name,
                    HeaderConventions.weights_column: result[HeaderConventions.cleaned_weights_column],
                    HeaderConventions.expected_annual_return_column: np.nan,
                    HeaderConventions.annual_volatility_column: np.nan,
                    HeaderConventions.sharpe_ratio_column: np.nan}
            else:
                result_dict = {
                    HeaderConventions.expected_return_column: expected_return_type,
                    HeaderConventions.risk_model_column: risk_model_name,
                    HeaderConventions.optimizer_column: optimizer_name,
                    HeaderConventions.weights_column: result[HeaderConventions.cleaned_weights_column],
                    HeaderConventions.expected_annual_return_column: result[
                        HeaderConventions.expected_annual_return_column],
                    HeaderConventions.annual_volatility_column: result[HeaderConventions.annual_volatility_column],
                    HeaderConventions.sharpe_ratio_column: result[HeaderConventions.sharpe_ratio_column]
                }
            results.append(result_dict)
    except Exception as e:
        logger.error(
            f"processing optimizer results for current_date=`{current_month_dir}`,Risk Model=`{risk_model_name}`, "
            f",Return Type=`{expected_return_type}`" + f" failed with error: {e}")
    return results


@ExecutionTimeRecorder(module_name=__name__)
def calculate_optimizations_for_risk_model(expected_return_df, risk_return_dict, data, current_month_dir):
    """
    Calculate optimizations for all risk models and expected return types.
    """
    module_name = os.path.basename(os.path.dirname(__file__))
    returns_cfg = load_config(module_name)
    enabled_methods = returns_cfg.optimization.enabled_methods
    logger.info("loading optmizers config for enabled_methods: %s", enabled_methods)

    all_results = []
    for expected_return_type in expected_return_df.columns:
        mu = expected_return_df[expected_return_type]

        for risk_model_name, cov_matrix in risk_return_dict.items():
            if cov_matrix.shape[0] == mu.shape[0]:
                results = process_optimizer_results(expected_return_type,
                                                    risk_model_name,
                                                    mu,
                                                    cov_matrix,
                                                    data,
                                                    current_month_dir,
                                                    enabled_methods)
                all_results.extend(results)
    return pd.DataFrame(all_results)


# Assuming df is your DataFrame
def clean_metadata(value):
    if isinstance(value, pd.Series):
        return value.values  # Extract just the values
    elif isinstance(value, list):
        return [str(v) for v in value]  # Convert each element to string for clarity
    return value


def extract_value(value):
    # Check if the value is a list and has only one element, then extract it
    # print(type(value))
    if isinstance(value, (np.ndarray, list)) and len(value) == 1:
        return value[0]
    # elif isinstance(value, tuple) and len(value) >= 2:
    #   return value[1]
    return value  # Return the value as-is if not a list


@ExecutionTimeRecorder(module_name=__name__)
def calculate_optimizations(data, expected_return_df, risk_return_dict, current_month_dir):
    """
    Iterate over each return type and risk model to calculate optimizations.
    """
    logger.info("calculating optimizations for the month {}".format(current_month_dir))

    if not risk_return_dict:
        logger.critical(
            "No risk models found. Skipping optimization calculations.Please check risk_return generated,"
            "no risk return was generated..")
        return None

    optimization_data = calculate_optimizations_for_risk_model(expected_return_df,
                                                               risk_return_dict,
                                                               data,
                                                               current_month_dir)

    # Clean the metadata and extract the values from the DataFrame
    df1 = optimization_data.apply(lambda x: x.map(clean_metadata))
    optimization_data_cleaned = df1.apply(lambda x: x.map(extract_value))

    return optimization_data_cleaned
