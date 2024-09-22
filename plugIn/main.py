import logging
import os
from pathlib import Path

import pandas as pd
from tabulate import tabulate

from logging_config import setup_logging
from plugIn.expected_return.main import calculate_all_returns
from plugIn.get_stocks import get_stocks
from plugIn.monte_carlo_simulation import run_monte_carlo_simulation
from plugIn.optimization.main import calculate_optimizations
from plugIn.performance.calculate_performance import calculate_performance
from plugIn.processing_weight.main import run_all_post_processing_weight
from plugIn.risk_returns.main import calculate_all_risk_matrix
from plugIn.utils import clean_up

pd.set_option('display.max_colwidth', None)  # Display full content in cells

setup_logging()
logger = logging.getLogger(__name__)
output_dir = Path(r"D:\PortfoliOpt\data")
pkl_filepath = os.path.join(output_dir, "results.pkl")
allocation_pkl_filepath = os.path.join(output_dir, "allocation.pkl")
performance_pkl_filepath = os.path.join(output_dir, "performance.pkl")

if __name__ == "__main__":
    data = get_stocks()
    expected_return_df = calculate_all_returns(data)
    risk_return_dict = calculate_all_risk_matrix(data)
    results_df = calculate_optimizations(data, expected_return_df, risk_return_dict)

    clean_up(results_df)
    results_df = run_monte_carlo_simulation(data, results_df)
    results_df.to_pickle(pkl_filepath)

    allocation_df = run_all_post_processing_weight(results_df, data)
    allocation_df.to_pickle(allocation_pkl_filepath)

    performance_df = calculate_performance(allocation_df, data, '2024-01-01', '2024-07-29')
    print(tabulate(performance_df, headers='keys', tablefmt='grid'))
    performance_df.to_pickle(performance_pkl_filepath)
