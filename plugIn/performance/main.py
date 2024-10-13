import logging

from plugIn.common.conventions import PklFileConventions
from plugIn.performance.calculate_performance import DefaultPerformance
from plugIn.common.utils import load_data_from_pickle, save_data_to_pickle

logger = logging.getLogger(__name__)


def calculate_performance(post_processing_df, data, start_date, end_date, current_month_dir):
    """Calculate and append performance metrics for portfolios based on allocation columns."""

    logger.info(f"started calculating calculate_performance for the month {current_month_dir}")
    performance_pkl_filepath = current_month_dir / PklFileConventions.performance_pkl_filename
    performance_df = load_data_from_pickle(performance_pkl_filepath)
    if performance_df is not None:
        return performance_df

    for index, row in post_processing_df.iterrows():
        for col in post_processing_df.columns:
            if col.startswith('Allocation_') and '_remaining_amount' not in col:
                allocation = row[col]  # Get the allocation dictionary
                remaining_amount_col = col.replace('weight', 'remaining_amount')
                remaining_amount = row[remaining_amount_col] if remaining_amount_col in row else 0

                # Use DefaultPerformance class
                performance = DefaultPerformance(allocation, data, remaining_amount)
                start_date, end_date = performance.check_dates(start_date, end_date)
                # # Calculate performance metrics
                portfolio_return = performance.calculate_return(start_date, end_date)
                portfolio_volatility = performance.calculate_volatility()
                portfolio_sharpe = performance.calculate_sharpe_ratio(start_date, end_date)

                # # Append performance metrics to the DataFrame
                method_name = col.split('_')[1]  # Extract method name (Greedy or LP)
                # Ensure you're working with a copy if post_processing_df is a slice
                post_processing_df = post_processing_df.copy()

                # Then perform your assignments
                post_processing_df.loc[index, f'{method_name}_Return'] = portfolio_return
                post_processing_df.loc[index, f'{method_name}_Volatility'] = portfolio_volatility
                post_processing_df.loc[index, f'{method_name}_Sharpe'] = portfolio_sharpe

    save_data_to_pickle(performance_pkl_filepath, post_processing_df)
    logger.info(f"completed calculating calculate_performance for the month {current_month_dir}")
    return post_processing_df
