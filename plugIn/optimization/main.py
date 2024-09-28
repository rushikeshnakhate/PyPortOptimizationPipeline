import logging

import pandas as pd

from plugIn.optimization.py_portfolio_op_frontier import PyPortfolioOptFrontier, PyPortfolioOptFrontierWithShortPosition
from plugIn.optimization.riskfolio_lib_frontier import MVRiskFolioOptimizer, MADRiskFolioOptimizer, \
    MSVRiskFolioOptimizer, FLPMRiskFolioOptimizer, SLPMRiskFolioOptimizer, CVaRRiskFolioOptimizer, \
    EVaRRiskFolioOptimizer, WRRiskFolioOptimizer, MDDRiskFolioOptimizer, ADDRiskFolioOptimizer, CDaRRiskFolioOptimizer, \
    UCIRiskFolioOptimizer, EDaRRiskFolioOptimizer

logger = logging.getLogger(__name__)


def get_all_efficient_frontier_optimizer(expected_returns, covariance_matrix, data=None):
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

    # Loop through each risk model, calculate the covariance matrix, and store it
    for optimizer, optimizer_name in optimizers.items():
        optimizer_instance = optimizer_name(expected_returns, covariance_matrix, data)
        optimizer_instance.calculate_efficient_frontier()
        optimizer_results = optimizer_instance.get_results()
        optimizers_dict[optimizer] = optimizer_results
    return optimizers_dict


def calculate_optimizations(data, expected_return_df, risk_return_dict):
    """
    Iterate over each return type and risk model to calculate optimizations.
    """
    all_results = []
    for return_type in expected_return_df.columns:
        mu = expected_return_df[return_type]

        for risk_model_name, cov_matrix in risk_return_dict.items():
            if cov_matrix.shape[0] == mu.shape[0]:
                results = process_optimizer_results(return_type, risk_model_name, mu, cov_matrix, data)
                all_results.extend(results)
    return pd.DataFrame(all_results)


def process_optimizer_results(return_type, risk_model_name, mu, cov_matrix, data):
    """
    Process the optimizer results for a given return type and risk model.
    """
    results = []
    try:
        logger.info(f"Calculating efficient frontier for Risk Model: {risk_model_name}, Return Type: {return_type}")
        optimizer_results = get_all_efficient_frontier_optimizer(mu, cov_matrix, data)

        for optimizer_name, result in optimizer_results.items():
            result_dict = {
                'Expected Return Type': return_type,
                'Risk Model': risk_model_name,
                'Optimizer': optimizer_name,
                'Weights': result['Cleaned_Weights'],
                'Expected Annual Return': result['Expected Annual Return'],
                'Annual Volatility': result['Annual Volatility'],
                'Sharpe Ratio': result['Sharpe Ratio']
            }
            results.append(result_dict)

    except Exception as e:
        logger.error(f"Error processing {return_type} with {risk_model_name}: {e}")
    return results

# if __name__ == "__main__":
#     output_dir = Path(r"D:\PortfoliOpt\data")
#     start_date = '2024-01-01'
#     end_date = '2024-01-10'
#     data = get_stocks(start_date, end_date, output_dir)
#     expected_return_df = calculate_all_returns(data)
#     risk_return_dict = calculate_all_risk_matrix(data)
#     results_df = calculate_optimizations(data, expected_return_df, risk_return_dict)
#     print(tabulate(results_df, headers='keys', tablefmt='grid'))
