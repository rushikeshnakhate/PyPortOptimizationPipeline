import os

import pandas as pd
import logging
from pathlib import Path
from tabulate import tabulate

from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.common.logging_config import setup_logging
from src.common.utils import create_current_data_directory
from src.dataDownloader.main import get_data
from src.date_generation.generate_date_ranges import generate_date_ranges
from src.expected_return.main import calculate_or_get_all_return
from src.experimental.monte_carlo_simulation import run_monte_carlo_simulation
from src.optimization.main import calculate_optimizations
from src.performance_metrics.main import calculate_performance
from src.processing_weight.main import run_all_post_processing_weight
from src.risk_returns.main import calculate_all_risk_matrix

# Setup logging
logger = logging.getLogger(__name__)

project_directory = Path(__file__).resolve().parent.parent
setup_logging(project_directory)


@ExecutionTimeRecorder(module_name=__name__)
def run_optimization_pipeline(
        years,  # List of years to process (mandatory)
        tickers=None,  # List of tickers(optional)
        frequency="yearly",  # Frequency (optional)
        data_directory=project_directory / "data",
        months=None,  # List of Months, if not provided then for all months of years(optional)
        expected_return_methods=None,  # Function to calculate expected returns
        risk_return_methods=None,  # Function to calculate risk return matrix
        optimization_methods=None,  # Function to calculate optimizations
        post_processing_methods=None  # Function for post-processing
):
    """
    This function runs the entire optimization pipeline with user-defined methods.

    Arguments:
    - years: List of years to process. If None, uses default configuration value.
    - months: List of months to process. If None, uses default configuration value.
    - frequency: Frequency of data (e.g., 'yearly', 'monthly' ,'multiyear). Default is 'yearly'.
    - expected_return_method: Function to calculate expected returns.
    - risk_return_method: Function to calculate risk return matrix (e.g., covariance matrix).
    - optimization_method: Function to calculate optimizations.
    - post_processing_method: Function for post-processing optimization weights.
    - performance_method: Function to calculate performance.

    Returns:
    - performance_df: The performance DataFrame after running the optimization pipeline.
    """

    # Generate date ranges based on user input or defaults

    date_ranges = generate_date_ranges(years=years, months=months, frequency=frequency)

    if date_ranges is None:
        raise Exception(
            f"Date ranges generation failed for years={years}, months={months}, frequency={frequency}"
        )

    # Loop through date ranges and process the data
    for start_date, end_date in date_ranges:
        current_dir = create_current_data_directory(start_date=start_date,
                                                    end_date=end_date,
                                                    output_dir=data_directory,
                                                    frequency=frequency)

        logger.info(f"Processing start_date={start_date}, end_date={end_date} for current_dir={current_dir}")

        # Load data for the given date range
        data = get_data(current_dir=current_dir, start_date=start_date, end_date=end_date, tickers=tickers)

        # Calculate expected returns using the provided method
        expected_return_df = calculate_or_get_all_return(data=data,
                                                         current_dir=current_dir,
                                                         enabled_methods=expected_return_methods)

        # Calculate risk return matrix using the provided method
        risk_return_dict = calculate_all_risk_matrix(data=data,
                                                     current_dir=current_dir,
                                                     enabled_methods=risk_return_methods)

        # Perform optimization using the provided method
        optimized_df = calculate_optimizations(data=data,
                                               expected_return_df=expected_return_df,
                                               risk_return_dict=risk_return_dict,
                                               current_dir=current_dir,
                                               enabled_methods=optimization_methods)

        # Run Monte Carlo simulation
        monte_carlo_df = run_monte_carlo_simulation(output_dir=current_dir, data=data)

        # Combine the optimization and Monte Carlo results
        all_optimized_df = pd.concat([monte_carlo_df, optimized_df], ignore_index=True)

        # Save the results to a pickle file
        save_pickle = Path(current_dir) / 'all_optimized_df.pkl'
        all_optimized_df.to_pickle(save_pickle)

        # Run post-processing on the optimized weights using the provided method
        post_processing_wright_df = run_all_post_processing_weight(results_df=all_optimized_df,
                                                                   data=data,
                                                                   current_dir=current_dir,
                                                                   enabled_methods=post_processing_methods)

        # Calculate performance based on the post-processed data
        performance_df = calculate_performance(post_processing_df=post_processing_wright_df,
                                               data=data,
                                               start_date=start_date,
                                               end_date=end_date,
                                               current_dir=current_dir)

        # Print a preview of the performance
        print(tabulate(performance_df.head(2), headers='keys', tablefmt='pretty'))


if __name__ == "__main__":
    run_optimization_pipeline(years=[2020], months=[1, 2], frequency="monthly")
    executionTimeRecorder_df = ExecutionTimeRecorder.get_performance_dataframe()
    executionTimeRecorder_df.to_pickle(Path(project_directory) / 'execution_timeppkl')
