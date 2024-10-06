import logging
from pathlib import Path

import pandas as pd
from tabulate import tabulate

from logging_config import setup_logging
from plugIn.expected_return.main import calculate_or_get_all_return
from plugIn.experimental.monte_carlo_simulation import run_monte_carlo_simulation
from plugIn.get_stocks import get_stocks
from plugIn.optimization.main import calculate_optimizations
from plugIn.performance.calculate_performance import calculate_performance
from plugIn.processing_weight.main import run_all_post_processing_weight
from plugIn.risk_returns.main import calculate_all_risk_matrix
from plugIn.utils import clean_up, generate_month_date_ranges, create_current_month_directory

pd.set_option('display.max_colwidth', None)  # Display full content in cells

setup_logging()
logger = logging.getLogger(__name__)
output_dir = Path(r"D:\PortfoliOpt\data")

if __name__ == "__main__":
    year = 2023
    rerun = True

    # Generate date ranges for each month in 2023
    # month_ranges = generate_month_date_ranges(year)
    month_ranges = generate_month_date_ranges(2023, months=[1, 12])
    # month_ranges = generate_month_date_ranges(2023)
    for start_date, end_date in month_ranges:
        logger.info(f"Processing start_date={start_date}, end_date={end_date}")
        current_month_dir = create_current_month_directory(start_date, output_dir)
        data = get_stocks(start_date, end_date, current_month_dir)

        expected_return_df = calculate_or_get_all_return(data, current_month_dir)
        risk_return_dict = calculate_all_risk_matrix(data, current_month_dir)

        optimized_df = calculate_optimizations(data, expected_return_df, risk_return_dict, current_month_dir)
        monte_carlo_df = run_monte_carlo_simulation(output_dir, data)
        all_optimized_df = pd.concat([monte_carlo_df, optimized_df], ignore_index=True)
        post_processing_wright_df = run_all_post_processing_weight(optimized_df, data, current_month_dir)
        # performance_df = calculate_performance(all_optimized_df, data, current_month_dir)
