import logging
import os
from pathlib import Path

import pandas as pd

from src.common.conventions import PklFileConventions
from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.common.hydra_config_loader import load_config
from src.risk_returns.exponential_covariance import ExponentialCovariance
from src.risk_returns.graphical_lasso import GraphicalLassoRiskModel
from src.risk_returns.ledoit_wolf_constant_correlation import LedoitWolfConstantCorrelation
from src.risk_returns.ledoit_wolf_constant_variance import LedoitWolfConstantVariance
from src.risk_returns.ledoit_wolf_shrinkage import LedoitWolfShrinkage
from src.risk_returns.ledoit_wolf_single_factor import LedoitWolfSingleFactor
from src.risk_returns.oracle_approximating_shrinkage import OracleApproximatingShrinkage

from src.risk_returns.risk_models_machine_learning import RegimeSwitchingRiskModel, \
    RandomForestVolatility, GaussianProcessRiskModel, SVMVolatility, KMeansClustering, CopulaRiskModel
from src.risk_returns.sample_covariance import SampleCovariance
from src.risk_returns.semi_covariance import SemiCovariance

logger = logging.getLogger(__name__)


def get_pickle_file_path(risk_type, output_dir: str):
    """
    Get the file path for the covariance matrix pickle file.
    """
    # Generate the file path with the updated pattern
    return os.path.join(output_dir,
                        PklFileConventions.ending_pattern_for_risk_return_pkl_files.format(risk_return_type=risk_type))


# Function to check if covariance matrix pickle file exists
def check_existing_cov_matrix(risk_type, output_dir):
    """
    Check if the covariance matrix for the given risk model already exists as a .pkl file.
    """
    pkl_filepath = get_pickle_file_path(risk_type,
                                        output_dir)
    if os.path.exists(pkl_filepath):
        logger.info(f"Loading covariance matrix for {risk_type} from {pkl_filepath}...")
        return pd.read_pickle(pkl_filepath)  # Load the matrix from pickle file
    return None  # File doesn't exist


# Function to save covariance matrix to a pickle file
def save_cov_matrix_to_pkl(cov_matrix, risk_type, output_dir):
    """
    Save the covariance matrix as a .pkl file for future use.
    """
    pkl_filepath = get_pickle_file_path(risk_type, output_dir)
    logger.info(f"Saving covariance matrix for {risk_type} to {pkl_filepath}...")
    pd.DataFrame(cov_matrix).to_pickle(pkl_filepath)


# Function to calculate the covariance matrix for each risk model
def calculate_cov_matrix(calculator):
    """
    Calculate the covariance matrix using the provided risk model calculator.
    """
    logger.info(f"Calculating covariance matrix...")
    return calculator.calculate_risk_matrix()


# Function to loop through the risk models
def process_risk_models(risk_model_calculators, output_dir, enabled_methods):
    """
    Loop through each risk model, calculate or load the covariance matrix, and store it.
    """
    # Dictionary to store covariance matrices for each risk model
    covariance_dict = {}

    module_name = os.path.basename(os.path.dirname(__file__))
    returns_cfg = load_config(module_name)
    if enabled_methods is None:
        enabled_methods = returns_cfg.risk_models.enabled_methods
    logger.info("loading risk_models config for enabled_methods: %s", enabled_methods)
    for enabled_method in enabled_methods:
        if enabled_method in risk_model_calculators:
            calculator = risk_model_calculators[enabled_method]
            # Check if the covariance matrix exists
            cov_matrix = check_existing_cov_matrix(enabled_method, output_dir)

            # If the file doesn't exist, calculate the covariance matrix and save it
            if cov_matrix is None:
                cov_matrix = calculate_cov_matrix(calculator)
                save_cov_matrix_to_pkl(cov_matrix, enabled_method, output_dir)

            # Store the covariance matrix in the dictionary
            covariance_dict[enabled_method] = pd.DataFrame(cov_matrix)
        else:
            logger.warning(
                f"No support for risk_return=`{enabled_method}`,Please add support OR remove from config.yaml.Support "
                f"available for risk_model_calculators={risk_model_calculators}")
    return covariance_dict


@ExecutionTimeRecorder(module_name=__name__)  # Use __name__ t
# Main function that orchestrates everything
def calculate_all_risk_matrix(data: pd.DataFrame, current_dir: Path, enabled_methods=None):
    """
    Calls different risk models, calculates the covariance matrices if not already saved,
    and saves them as .pkl files for future use.
    """
    # Ensure the output directory exists
    os.makedirs(current_dir, exist_ok=True)

    # Create a dictionary of risk model types and their corresponding classes
    risk_model_calculators = {
        'SampleCovariance': SampleCovariance(data),
        'SemiCovariance': SemiCovariance(data),
        'ExponentialCovariance': ExponentialCovariance(data),
        'LedoitWolfShrinkage': LedoitWolfShrinkage(data),
        'LedoitWolfConstantVariance': LedoitWolfConstantVariance(data),
        'LedoitWolfSingleFactor': LedoitWolfSingleFactor(data),
        'LedoitWolfConstantCorrelation': LedoitWolfConstantCorrelation(data),
        'OracleApproximatingShrinkage': OracleApproximatingShrinkage(data),
        'GraphicalLasso': GraphicalLassoRiskModel(data),
        'RandomForestVolatility': RandomForestVolatility(data),
        'GaussianProcessRiskModel': GaussianProcessRiskModel(data),
        'SVMVolatility': SVMVolatility(data),
        'KMeansClustering': KMeansClustering(data),
        'CopulaRiskModel': CopulaRiskModel(data),
        'RegimeSwitchingRiskModel': RegimeSwitchingRiskModel(data),
        # 'AutoencoderRiskModel': AutoencoderRiskModel(data),
    }

    # Call the process function to loop through the risk models and calculate/save covariance matrices
    return process_risk_models(risk_model_calculators, current_dir, enabled_methods)
