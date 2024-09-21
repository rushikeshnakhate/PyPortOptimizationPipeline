import os

import pandas as pd

from plugIn.risk_returns.risk_models import SampleCovariance, SemiCovariance, ExponentialCovariance, \
    LedoitWolfShrinkage, LedoitWolfConstantVariance, LedoitWolfSingleFactor, OracleApproximatingShrinkage, \
    LedoitWolfConstantCorrelation, PCARiskModel, GraphicalLassoRiskModel

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
# Set environment variables to control OpenMP behavior
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

from plugIn.risk_returns.risk_models_machine_learning import RegimeSwitchingRiskModel, AutoencoderRiskModel, \
    RandomForestVolatility, GaussianProcessRiskModel, SVMVolatility, KMeansClustering, CopulaRiskModel


def calculate_all_risk_matrix(data):
    """
    Calls different risk models and stores their covariance matrices.
    """
    # Create a dictionary of risk model types and their corresponding classes
    risk_model_calculators = {
        'SampleCovariance': SampleCovariance(data),
        # 'SemiCovariance': SemiCovariance(data),
        # 'ExponentialCovariance': ExponentialCovariance(data),
        # 'LedoitWolfShrinkage': LedoitWolfShrinkage(data),
        # 'LedoitWolfConstantVariance': LedoitWolfConstantVariance(data),
        # 'LedoitWolfSingleFactor': LedoitWolfSingleFactor(data),
        # 'LedoitWolfConstantCorrelation': LedoitWolfConstantCorrelation(data),
        # 'OracleApproximatingShrinkage': OracleApproximatingShrinkage(data),
        # # 'PCARiskModel': PCARiskModel(data),
        # 'GraphicalLasso': GraphicalLassoRiskModel(data),
        # # Machine learning-based risk models
        # 'AutoencoderRiskModel': AutoencoderRiskModel(data),
        # 'RandomForestVolatility': RandomForestVolatility(data),
        # 'GaussianProcessRiskModel': GaussianProcessRiskModel(data),
        # 'SVMVolatility': SVMVolatility(data),
        # 'KMeansClustering': KMeansClustering(data),
        # 'CopulaRiskModel': CopulaRiskModel(data),
        'RegimeSwitchingRiskModel': RegimeSwitchingRiskModel(data),
        # 'BayesianNetworkRiskModel': BayesianNetworkRiskModel(data),
        # 'NeuralNetworkVolatility': NeuralNetworkVolatility(data),
        # 'GARCHRiskModel': GARCHRiskModel(data),
    }

    # Dictionary to store covariance matrices for each risk model
    covariance_dict = {}

    # Loop through each risk model, calculate the covariance matrix, and store it
    for risk_type, calculator in risk_model_calculators.items():
        print(f"Calculating {risk_type}...")
        cov_matrix = calculator.calculate_risk_matrix()
        covariance_dict[risk_type] = pd.DataFrame(cov_matrix)
    return covariance_dict
