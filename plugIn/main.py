import logging
from pathlib import Path

import pandas as pd

from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.common.logging_config import setup_logging
from plugIn.common.utils import generate_month_date_ranges, create_current_month_directory
from plugIn.dataDownloader.get_stocks import get_stocks
from plugIn.expected_return.main import calculate_or_get_all_return
from plugIn.experimental.monte_carlo_simulation import run_monte_carlo_simulation
from plugIn.optimization.main import calculate_optimizations
from plugIn.performance.main import calculate_performance
from plugIn.processing_weight.main import run_all_post_processing_weight
from plugIn.risk_returns.main import calculate_all_risk_matrix

pd.set_option('display.max_colwidth', None)  # Display full content in cells

setup_logging()
logger = logging.getLogger(__name__)
output_dir = Path(r"D:\PortfoliOpt\data")
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    year = 2023
    month_ranges = generate_month_date_ranges(year, months=[1])
    # month_ranges = generate_month_date_ranges(2023)
    for start_date, end_date in month_ranges:
        current_month_dir = create_current_month_directory(start_date, output_dir)
        logger.info(
            f"Processing start_date={start_date}, end_date={end_date} for current_month_dir={current_month_dir}")
        data = get_stocks(start_date, end_date, current_month_dir)

        expected_return_df = calculate_or_get_all_return(data, current_month_dir)
        risk_return_dict = calculate_all_risk_matrix(data, current_month_dir)
        optimized_df = calculate_optimizations(data, expected_return_df.head(10), risk_return_dict, current_month_dir)
        monte_carlo_df = run_monte_carlo_simulation(output_dir, data)
        all_optimized_df = pd.concat([monte_carlo_df, optimized_df], ignore_index=True)
        post_processing_wright_df = run_all_post_processing_weight(optimized_df, data, current_month_dir)
        performance_df = calculate_performance(post_processing_wright_df, data, start_date, end_date,
                                               current_month_dir)
        # print(tabulate(optimized_df.head(20), headers='keys', tablefmt='pretty'))

        ExecutionTimeRecorder.print_results()
# if __name__ == "__main__":
#     rerun = True
#     if __name__ == "__main__":
#         cProfile.run('main()', 'profiling_stats')
#         stats = pstats.Stats('profiling_stats')
#         # Sort by cumulative time and print the top 10
#         stats.sort_stats('cumulative').print_stats(10)
