import ast
import logging

from src.common.conventions import PklFileConventions
from src.common.utils import load_data_from_pickle, save_data_to_pickle
from src.performance_metrics.performance_metrics_name_convernsions import PerformanceMetricsNameConventions
from src.performance_metrics.portfoliio_performance import PortfolioWithAllocatedWeights
from src.performance_metrics.portfolio_return import PortfolioReturn
from src.performance_metrics.portfolio_sharpratio import PortfolioSharpeRatio
from src.performance_metrics.portfolio_volatility import PortfolioVolatility

logger = logging.getLogger(__name__)


def calculate_performance(post_processing_df, data, start_date, end_date, current_dir):
    """Calculate and append performance_metrics metrics for portfolios based on allocation columns."""

    logger.info(f"started calculating calculate_performance for the month {current_dir}")
    performance_pkl_filepath = current_dir / PklFileConventions.performance_pkl_filename
    performance_df = load_data_from_pickle(performance_pkl_filepath)
    # if performance_df is not None:
    #     return performance_df

    for index, row in post_processing_df.iterrows():
        for col in post_processing_df.columns:
            if col.startswith('Allocation_') and '_remaining_amount' not in col:
                try:
                    # Safely convert string to dictionary
                    allocation_str = row[col]  # Get the allocation dictionary
                    # Replace NaN with None for safe evaluation
                    allocation_str = allocation_str.replace("NaN", "None") if isinstance(allocation_str,
                                                                                         str) else allocation_str
                    allocation_dict = ast.literal_eval(allocation_str)

                    remaining_amount_col = col.replace('weight', 'remaining_amount')
                    remaining_amount = row[remaining_amount_col] if remaining_amount_col in row else 0

                    portfolio = PortfolioWithAllocatedWeights(allocation_dict, data, remaining_amount)
                    parameters_config = {'start_date': start_date, 'end_date': end_date}

                    precalculated_metrics = {
                        PerformanceMetricsNameConventions.portfolio_volatility: PortfolioVolatility().calculate(
                            portfolio),
                        PerformanceMetricsNameConventions.portfolio_return: PortfolioReturn(
                            parameters_config).calculate(
                            portfolio),
                    }

                    portfolio_sharpe_ratio = PortfolioSharpeRatio(parameters_config).calculate(portfolio,
                                                                                               precalculated_metrics)

                    # # Append performance_metrics metrics to the DataFrame
                    method_name = col.split('_')[1]  # Extract method name (Greedy or LP)
                    # Ensure you're working with a copy if post_processing_df is a slice
                    post_processing_df = post_processing_df.copy()

                    # Then perform your assignments
                    post_processing_df.loc[index, f'{method_name}_Volatility'] = precalculated_metrics.get(
                        PerformanceMetricsNameConventions.portfolio_volatility)
                    post_processing_df.loc[index, f'{method_name}_Return'] = precalculated_metrics.get(
                        PerformanceMetricsNameConventions.portfolio_return)
                    post_processing_df.loc[index, f'{method_name}_Sharpe'] = portfolio_sharpe_ratio
                except Exception as ex:
                    logger.warning(
                        "exception={}, skipping performance calculation for index={},row={}".format(ex, index,
                                                                                                    row[col]))
                # post_processing_df.dropna()
    save_data_to_pickle(performance_pkl_filepath, post_processing_df)
    logger.info(f"completed calculating calculate_performance for the month {current_dir}")
    return post_processing_df
