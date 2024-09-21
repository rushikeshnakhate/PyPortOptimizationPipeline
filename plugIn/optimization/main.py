from plugIn.optimization.py_portfolio_op_frontier import PyPortfolioOptFrontier, PyPortfolioOptFrontierWithShortPosition
from plugIn.optimization.riskfolio_lib_frontier import RiskfolioLibFrontier


def get_all_efficient_frontier_optimizer(expected_returns, covariance_matrix, data=None):
    optimizers = {
        'pyPortfolioOptFrontier': PyPortfolioOptFrontier,
        'pyPortfolioOptFrontierWithShortPosition': PyPortfolioOptFrontierWithShortPosition,
        'riskfolio-lib': RiskfolioLibFrontier,
        # Add more optimizers here as needed
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
