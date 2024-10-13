import logging
import os
import pandas as pd

from plugIn.common.conventions import PklFileConventions
from plugIn.risk_returns.exponential_covariance import ExponentialCovariance
from plugIn.risk_returns.graphical_lasso import GraphicalLassoRiskModel
from plugIn.risk_returns.ledoit_wolf_constant_correlation import LedoitWolfConstantCorrelation
from plugIn.risk_returns.ledoit_wolf_constant_variance import LedoitWolfConstantVariance
from plugIn.risk_returns.ledoit_wolf_shrinkage import LedoitWolfShrinkage
from plugIn.risk_returns.ledoit_wolf_single_factor import LedoitWolfSingleFactor
from plugIn.risk_returns.oracle_approximating_shrinkage import OracleApproximatingShrinkage

from plugIn.risk_returns.risk_models_machine_learning import RegimeSwitchingRiskModel, AutoencoderRiskModel, \
    RandomForestVolatility, GaussianProcessRiskModel, SVMVolatility, KMeansClustering, CopulaRiskModel
from plugIn.risk_returns.sample_covariance import SampleCovariance
from plugIn.risk_returns.semi_covariance import SemiCovariance

logger = logging.getLogger(__name__)


# Function to check if covariance matrix pickle file exists
def check_existing_cov_matrix(risk_type, output_dir):
    """
    Check if the covariance matrix for the given risk model already exists as a .pkl file.
    """
    pkl_filepath = os.path.join(output_dir,
                                f"{risk_type}_{PklFileConventions.ending_pattern_for_risk_return_pkl_files}")

    if os.path.exists(pkl_filepath):
        logger.info(f"Loading covariance matrix for {risk_type} from {pkl_filepath}...")
        return pd.read_pickle(pkl_filepath)  # Load the matrix from pickle file
    return None  # File doesn't exist


# Function to save covariance matrix to a pickle file
def save_cov_matrix_to_pkl(cov_matrix, risk_type, output_dir):
    """
    Save the covariance matrix as a .pkl file for future use.
    """
    pkl_filepath = os.path.join(output_dir,
                                f"{risk_type}_{PklFileConventions.ending_pattern_for_risk_return_pkl_files}")

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
def process_risk_models(risk_model_calculators, output_dir):
    """
    Loop through each risk model, calculate or load the covariance matrix, and store it.
    """
    # Dictionary to store covariance matrices for each risk model
    covariance_dict = {}

    for risk_type, calculator in risk_model_calculators.items():
        # Check if the covariance matrix exists
        cov_matrix = check_existing_cov_matrix(risk_type, output_dir)

        # If the file doesn't exist, calculate the covariance matrix and save it
        if cov_matrix is None:
            cov_matrix = calculate_cov_matrix(calculator)
            save_cov_matrix_to_pkl(cov_matrix, risk_type, output_dir)

        # Store the covariance matrix in the dictionary
        covariance_dict[risk_type] = pd.DataFrame(cov_matrix)

    return covariance_dict


# Main function that orchestrates everything
def calculate_all_risk_matrix(data, output_dir):
    """
    Calls different risk models, calculates the covariance matrices if not already saved,
    and saves them as .pkl files for future use.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

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
        'AutoencoderRiskModel': AutoencoderRiskModel(data),
        'RandomForestVolatility': RandomForestVolatility(data),
        'GaussianProcessRiskModel': GaussianProcessRiskModel(data),
        'SVMVolatility': SVMVolatility(data),
        'KMeansClustering': KMeansClustering(data),
        'CopulaRiskModel': CopulaRiskModel(data),
        'RegimeSwitchingRiskModel': RegimeSwitchingRiskModel(data),
    }

    # Call the process function to loop through the risk models and calculate/save covariance matrices
    return process_risk_models(risk_model_calculators, output_dir)

# Example usage
# if __name__ == "__main__":
#     data = pd.DataFrame()  # Replace with your actual data
#     output_dir = "./covariance_matrices"  # Directory to save/load covariance matrices
#     covariance_matrices = calculate_all_risk_matrix(data, output_dir)
