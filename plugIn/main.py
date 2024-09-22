import logging

import pandas as pd
from tabulate import tabulate

from logging_config import setup_logging
from plugIn.expected_return.main import calculate_all_returns
from plugIn.get_stocks import get_stocks
from plugIn.monte_carlo_simulation import run_monte_carlo_simulation
from plugIn.optimization.main import calculate_optimizations
from plugIn.risk_returns.main import calculate_all_risk_matrix
from plugIn.processing_weight.greedy_portfolio import GreedyPortfolio

pd.set_option('display.max_colwidth', None)  # Display full content in cells

setup_logging()
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    data = get_stocks()
    expected_return_df = calculate_all_returns(data)
    risk_return_dict = calculate_all_risk_matrix(data)
    results_df = calculate_optimizations(data, expected_return_df, risk_return_dict)
    results_df = run_monte_carlo_simulation(data, results_df)
    greedyPortfolio = GreedyPortfolio(results_df['Weights'], data.iloc[-1])
    df = greedyPortfolio.get_allocation()
    logger.info(tabulate(df, headers='keys', tablefmt='grid'))
