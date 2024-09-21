from logging_config import setup_logging
import logging
import pandas as pd
from tabulate import tabulate

from plugIn.expected_return.main import calculate_all_returns
from plugIn.get_stocks import get_stocks
from plugIn.monte_carlo_simulation import MonteCarloSimulation
from plugIn.optimization.main import get_all_efficient_frontier_optimizer
from plugIn.risk_returns.main import calculate_all_risk_matrix

pd.set_option('display.max_colwidth', None)  # Display full content in cells

setup_logging()
logger = logging.getLogger(__name__)


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


def run_monte_carlo_simulation(data, results_df):
    """
    Run the Monte Carlo simulation and append the results to the results DataFrame.
    """
    monte_carlo_simulation = MonteCarloSimulation(data)
    max_sharpe_ratio, min_volatility = monte_carlo_simulation.run_monte_carlo_simulation()
    results_df = pd.concat([results_df, max_sharpe_ratio], ignore_index=True)
    results_df = pd.concat([results_df, min_volatility], ignore_index=True)
    return results_df


if __name__ == "__main__":
    data = get_stocks()
    expected_return_df = calculate_all_returns(data)
    risk_return_dict = calculate_all_risk_matrix(data)
    results_df = calculate_optimizations(data, expected_return_df, risk_return_dict)
    results_df = run_monte_carlo_simulation(data, results_df)
    # Log the final results
    logger.info(tabulate(results_df, headers='keys', tablefmt='grid'))
