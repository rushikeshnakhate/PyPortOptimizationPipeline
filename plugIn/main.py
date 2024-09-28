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
expected_return_pkl_filepath = os.path.join(output_dir, "expected_return.pkl")
data_pkl_filepath = os.path.join(output_dir, "data.pkl")

if __name__ == "__main__":
    start_date = '2024-01-01'
    end_date = '2024-01-30'
    previous_end_date = '2024-01-29'
    rerun = True
    if rerun is None:
        data = get_stocks(start_date, end_date, output_dir)

        expected_return_df = calculate_all_returns(data)
        expected_return_df.to_pickle(expected_return_pkl_filepath)

        risk_return_dict = calculate_all_risk_matrix(data)
        results_df = calculate_optimizations(data, expected_return_df, risk_return_dict)
        results_df.to_pickle(pkl_filepath)

        clean_up(results_df)
        results_df = run_monte_carlo_simulation(data, results_df)
        results_df.to_pickle(pkl_filepath)
    else:
        data = pd.read_pickle(data_pkl_filepath)
        expected_return_df = pd.read_pickle(expected_return_pkl_filepath)
        risk_return_dict = calculate_all_risk_matrix(data)
        results_df = pd.read_pickle(pkl_filepath)

    allocation_df = run_all_post_processing_weight(results_df, data)
    allocation_df.to_pickle(allocation_pkl_filepath)

    performance_df = calculate_performance(allocation_df, data, start_date=start_date, end_date=previous_end_date)
    performance_df.to_pickle(performance_pkl_filepath)

    allocation_df = pd.read_pickle(allocation_pkl_filepath)
    print(tabulate(allocation_df.head(10), headers='keys', tablefmt='grid'))
