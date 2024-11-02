import logging
import os
from pathlib import Path

import pandas as pd
from tabulate import tabulate

from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.common.hydra_config_loader import load_config
from plugIn.common.logging_config import setup_logging
from plugIn.common.utils import generate_month_date_ranges, create_current_month_directory
from plugIn.dataDownloader.main import get_data

from plugIn.expected_return.main import calculate_or_get_all_return
from plugIn.experimental.monte_carlo_simulation import run_monte_carlo_simulation
from plugIn.optimization.main import calculate_optimizations
from plugIn.performance.main import calculate_performance
from plugIn.processing_weight.main import run_all_post_processing_weight
from plugIn.risk_returns.main import calculate_all_risk_matrix

pd.set_option('display.max_colwidth', None)  # Display full content in cells

module_name = os.path.basename(os.path.dirname(__file__))
configuration = load_config(module_name)
setup_logging(configuration.log_dir)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@ExecutionTimeRecorder(module_name=__name__)
def main():
    month_ranges = generate_month_date_ranges(configuration.year, months=configuration.months)
    for start_date, end_date in month_ranges:
        current_month_dir = create_current_month_directory(start_date, configuration.output_dir)
        logger.info(f"Processing start_date={start_date}, end_date={end_date} "
                    f"for current_month_dir={current_month_dir}")
        data = get_data(current_dir=current_month_dir, start_date=start_date, end_date=end_date)
        expected_return_df = calculate_or_get_all_return(data, current_month_dir)
        risk_return_dict = calculate_all_risk_matrix(data, current_month_dir)
        optimized_df = calculate_optimizations(data, expected_return_df.head(10), risk_return_dict, current_month_dir)
        print(tabulate(optimized_df, headers='keys', tablefmt='grid'))
        # monte_carlo_df = run_monte_carlo_simulation(configuration.output_dir, data)
        # all_optimized_df = pd.concat([monte_carlo_df, optimized_df], ignore_index=True)
        # post_processing_wright_df = run_all_post_processing_weight(all_optimized_df, data, current_month_dir)
        # performance_df = calculate_performance(post_processing_wright_df, data, start_date, end_date, current_month_dir)


if __name__ == "__main__":
    main()
    ExecutionTimeRecorder.print_results()
