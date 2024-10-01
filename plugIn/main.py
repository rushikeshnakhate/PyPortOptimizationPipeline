import logging
import os
from pathlib import Path

import pandas as pd
from tabulate import tabulate

from logging_config import setup_logging
from plugIn.expected_return.main import calculate_all_returns, calculate_or_get_all_return
from plugIn.get_stocks import get_stocks
from plugIn.monte_carlo_simulation import run_monte_carlo_simulation
from plugIn.optimization.main import calculate_optimizations
from plugIn.performance.calculate_performance import calculate_performance
from plugIn.processing_weight.main import run_all_post_processing_weight
from plugIn.risk_returns.main import calculate_all_risk_matrix
from plugIn.utils import clean_up, generate_month_date_ranges, create_current_month_directory

pd.set_option('display.max_colwidth', None)  # Display full content in cells

setup_logging()
logger = logging.getLogger(__name__)
output_dir = Path(r"D:\PortfoliOpt\data")
optimization_pkl_filepath = os.path.join(output_dir, "optimization.pkl")
post_processing_wright_pkl_filepath = os.path.join(output_dir, "post_processing_wright.pkl")
performance_pkl_filepath = os.path.join(output_dir, "performance.pkl")
expected_return_pkl_filepath = os.path.join(output_dir, "expected_return.pkl")
data_pkl_filepath = os.path.join(output_dir, "data.pkl")

if __name__ == "__main__":
    year = 2023
    rerun = True
    # Generate date ranges for each month in 2023
    month_ranges = generate_month_date_ranges(year)
    for start_date, end_date in month_ranges:
        logger.info(f"Processing start_date={start_date}, end_date={end_date}")
        current_month_dir = create_current_month_directory(start_date, output_dir)
        data = get_stocks(start_date, end_date, current_month_dir)

        expected_return_df = calculate_or_get_all_return(data, current_month_dir)

    #
    #     risk_return_dict = calculate_all_risk_matrix(data)
    #     optimized_df = calculate_optimizations(data, expected_return_df, risk_return_dict)
    #     clean_up(optimized_df)
    #     optimized_df = run_monte_carlo_simulation(data, optimized_df)
    #     optimized_df.to_pickle(optimization_pkl_filepath)
    #
    #     post_processing_wright_df = run_all_post_processing_weight(optimized_df, data)
    #     post_processing_wright_df.to_pickle(post_processing_wright_pkl_filepath)
    # else:
    #     data = pd.read_pickle(data_pkl_filepath)
    #     expected_return_df = pd.read_pickle(expected_return_pkl_filepath)
    #     risk_return_dict = calculate_all_risk_matrix(data)
    #     optimized_df = pd.read_pickle(optimization_pkl_filepath)
    #     post_processing_wright_df = pd.read_pickle(post_processing_wright_pkl_filepath)
    #     performance_df = pd.read_pickle(performance_pkl_filepath)
    #
    # performance_df = calculate_performance(post_processing_wright_df, data, start_date=start_date,
    #                                        end_date=previous_end_date)
    # performance_df.to_pickle(performance_pkl_filepath)
    # print(tabulate(post_processing_wright_df.head(10), headers='keys', tablefmt='grid'))
