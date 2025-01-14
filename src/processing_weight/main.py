import logging
import os
from pathlib import Path

import pandas as pd

from src.common.conventions import HeaderConventions, PklFileConventions
from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.common.hydra_config_loader import load_config
from src.processing_weight.custom_clustered_allocator import CustomClusteredAllocator
from src.processing_weight.custom_diversity_allocator import CustomDiversityAllocator
from src.processing_weight.custom_greedy_allocation import CustomGreedyAllocation
from src.processing_weight.custom_proportional_rounding_allocator import CustomProportionalRoundingAllocator
from src.processing_weight.custom_transaction_cost_allocator import CustomTransactionCostAllocator
from src.processing_weight.custom_wighted_floor_allocator import CustomWeightedFloorAllocator
from src.processing_weight.greedy_portfolio import GreedyPortfolio
from src.processing_weight.lp_portfolio import LpPortfolio
from src.common.utils import save_data_to_pickle, load_data_from_pickle

logger = logging.getLogger(__name__)


# Function to create allocation classes mapping (consider enabled methods)
def get_allocation_classes(enabled_methods):
    """
    Returns a dictionary of allocation types mapped to their respective portfolio classes,
    considering only the enabled methods.
    """
    if enabled_methods is None:
        enabled_methods = get_enabled_methods()
    allocation_classes = {
        'CustomClusteredAllocator': CustomClusteredAllocator,
        'CustomDiversityAllocator': CustomDiversityAllocator,
        'CustomGreedyAllocation': CustomGreedyAllocation,
        'CustomProportionalRoundingAllocator': CustomProportionalRoundingAllocator,
        'CustomTransactionCostAllocator': CustomTransactionCostAllocator,
        'CustomWeightedFloorAllocator': CustomWeightedFloorAllocator,
        'GreedyPortfolio': GreedyPortfolio,
        'LpPortfolio': LpPortfolio
        # Add more allocation classes here
    }
    return {allocation_type: portfolio_class for allocation_type, portfolio_class in allocation_classes.items() if
            allocation_type in enabled_methods}


# Function to process allocations for a single row and method
def process_post_processing_for_row_method(sr_no, row, data, portfolio_class, budget, total_rows):
    """
    Processes allocations for a single row and method, returns the allocation.
    """
    weights = row[HeaderConventions.weights_column]  # Get weights dictionary
    latest_prices = data.iloc[-1]  # Get latest prices

    try:
        logger.info(
            f"Running {portfolio_class.__name__} for Sr No={sr_no},"
            f" total portfolio={total_rows} with budget={budget}...")
        portfolio = portfolio_class(weights, latest_prices, budget)
        allocation = portfolio.get_allocation()  # Get allocation (tuple of (allocation dict, remaining amount))
        return allocation
    except Exception as e:
        logger.error(f"Error in {portfolio_class.__name__} for Sr No={sr_no}: {e}")
        return f"error at Sr No={sr_no}: {e}"


def do_process(budget, current_month_dir, data, post_processing_classes, results_df):
    total_rows = len(results_df)
    for sr_no, (index, row) in enumerate(results_df.iterrows(), start=1):
        logger.info(f"Processing row {sr_no}/{total_rows} for the month {current_month_dir}")

        for allocation_type, portfolio_class in post_processing_classes.items():
            allocation = process_post_processing_for_row_method(sr_no, row, data, portfolio_class, budget, total_rows)

            # Check if allocation is a tuple containing a dictionary and a scalar
            if isinstance(allocation, tuple) and len(allocation) == 2:
                allocation_dict, remaining_amount = allocation

                # Ensure allocation_dict and remaining_amount are valid before assigning
                if isinstance(allocation_dict, dict) and remaining_amount is not None:
                    # Convert allocation_dict to a string to store it in a single cell
                    results_df.loc[index, f'Allocation_{allocation_type}_weight'] = str(allocation_dict)
                    results_df.loc[index, f'Allocation_{allocation_type}_remaining_amount'] = remaining_amount
                else:
                    logger.error(f"Invalid allocation data for {allocation_type} at Sr No={sr_no}")
                    results_df.loc[index, f'Allocation_{allocation_type}_remaining_amount'] = "invalid allocation data"
            else:
                # In case of an error, log it in the DataFrame
                results_df.loc[index, f'Allocation_{allocation_type}_remaining_amount'] = allocation


def get_enabled_methods():
    module_name = os.path.basename(os.path.dirname(__file__))
    returns_cfg = load_config(module_name)
    enabled_methods = returns_cfg.processing_weights.enabled_methods
    logger.info("loading config for enabled_methods=%s", enabled_methods)
    return enabled_methods


@ExecutionTimeRecorder(module_name=__name__)
# Main function to process all rows
def run_all_post_processing_weight(results_df: pd.DataFrame,
                                   data: pd.DataFrame,
                                   current_dir: Path,
                                   enabled_methods=None,
                                   budget=1000000):
    """
    Processes all rows in the results DataFrame and adds post_processing to it, row-by-row, method-by-method.
    """
    logger.info(f"Calculating processing_weight for the month {current_dir}")
    post_processing_weight_pkl_filepath = current_dir / PklFileConventions.post_processing_weight_pkl_filename
    post_processing = load_data_from_pickle(post_processing_weight_pkl_filepath)
    if post_processing is not None:
        return post_processing
    post_processing_classes = get_allocation_classes(enabled_methods)
    do_process(budget, current_dir, data, post_processing_classes, results_df)
    save_data_to_pickle(post_processing_weight_pkl_filepath, results_df)
    logger.info("Processing weight completed successfully for the month {}".format(current_dir))
    return results_df
