import pandas as pd
from tabulate import tabulate

from plugIn.expected_return.main import get_expected_return
from plugIn.get_stocks import get_stocks
from plugIn.optimization.main import get_all_efficient_frontier_optimizer

from plugIn.risk_returns.main import calculate_all_risk_matrix
import pandas as pd

pd.set_option('display.max_colwidth', None)  # Display full content in cells

# Assuming results_df is already created from the previous code
from logging_config import setup_logging
import logging

setup_logging()

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    # Assuming data is already obtained
    data = get_stocks()
    expected_return_df = get_expected_return(data)
    risk_return_dict = calculate_all_risk_matrix(data)

    results = []
    for return_type in expected_return_df.columns:
        mu = expected_return_df[return_type]  # Expected returns for this type

        # Iterate over each risk model in risk_return_dict
        for risk_model_name, cov_matrix in risk_return_dict.items():
            # Ensure the covariance matrix and expected returns are aligned
            if cov_matrix.shape[0] == mu.shape[0]:
                try:
                    logger.info(
                        f"calculate efficient frontier risk_model_name{risk_model_name} return_type{return_type}")
                    # Get the optimization results for each optimizer
                    optimizer_results = get_all_efficient_frontier_optimizer(mu, cov_matrix, data)

                    # Store results in a dictionary and append it to the results list
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
                    continue
    results_df = pd.DataFrame(results)
    # Use tabulate to print the DataFrame with borders
    logger.info(tabulate(results_df, headers='keys', tablefmt='grid'))
