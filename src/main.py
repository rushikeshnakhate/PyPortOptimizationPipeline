import logging
import os
from pathlib import Path

import pandas as pd
from tabulate import tabulate

from src.common.conventions import GeneralConventions
from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.common.hydra_config_loader import load_config
from src.common.logging_config import setup_logging
from src.common.utils import generate_date_ranges, create_current_data_directory
from src.dataDownloader.main import get_data
from src.expected_return.main import calculate_or_get_all_return
from src.experimental.monte_carlo_simulation import run_monte_carlo_simulation
from src.optimization.main import calculate_optimizations
from src.performance_metrics.main import calculate_performance
from src.processing_weight.main import run_all_post_processing_weight
from src.risk_returns.main import calculate_all_risk_matrix

pd.set_option('display.max_colwidth', None)  # Display full content in cells

module_name = os.path.basename(os.path.dirname(__file__))
configuration = load_config(module_name)
setup_logging(configuration.log_dir)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@ExecutionTimeRecorder(module_name=__name__)
def main():
    frequency = GeneralConventions.frequency_yearly
    date_ranges = generate_date_ranges(year=configuration.year, months=configuration.months,
                                       frequency=frequency)
    if date_ranges is None:
        raise Exception(
            "date ranges generation failed for year={},months={},frequency={}".format(
                configuration.year, configuration.months, frequency))

    for start_date, end_date in date_ranges:
        current_dir = create_current_data_directory(start_date, configuration.output_dir, frequency)
        logger.info(f"Processing start_date={start_date}, end_date={end_date} "
                    f"for current_dir={current_dir}")
        data = get_data(current_dir=current_dir, start_date=start_date, end_date=end_date)
        expected_return_df = calculate_or_get_all_return(data, current_dir)
        risk_return_dict = calculate_all_risk_matrix(data, current_dir)
        optimized_df = calculate_optimizations(data, expected_return_df, risk_return_dict, current_dir)
        monte_carlo_df = run_monte_carlo_simulation(configuration.output_dir, data)
        all_optimized_df = pd.concat([monte_carlo_df, optimized_df], ignore_index=True)

        save_pickle = Path(current_dir) / 'all_optimized_df.pkl'
        all_optimized_df.to_pickle(save_pickle)
        post_processing_wright_df = run_all_post_processing_weight(all_optimized_df, data, current_dir)
        performance_df = calculate_performance(post_processing_wright_df, data, start_date, end_date,
                                               current_dir)
        print(tabulate(performance_df.head(2), headers='keys', tablefmt='pretty'))


if __name__ == "__main__":
    main()
    ExecutionTimeRecorder.print_results()
