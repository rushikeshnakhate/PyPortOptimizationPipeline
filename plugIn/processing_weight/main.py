import logging

import pandas as pd

from plugIn.conventions import HeaderConventions, PklFileConventions
from plugIn.processing_weight.greedy_portfolio import GreedyPortfolio
from plugIn.processing_weight.lp_portfolio import LpPortfolio
from plugIn.utils import save_data_to_pickle, load_data_from_pickle

logger = logging.getLogger(__name__)


# Function to create allocation classes mapping
def get_allocation_classes():
    """
    Returns a dictionary of allocation types mapped to their respective portfolio classes.
    """
    return {
        'GreedyPortfolio': GreedyPortfolio,
        'LpPortfolio': LpPortfolio,
    }


# Function to process allocations for a single row
def process_post_processing_for_row(sr_no, row, data, allocation_classes, budget, total_rows):
    """
    Processes allocations for a single row and returns a dictionary of allocations.
    """
    weights = row[HeaderConventions.weights_column]  # Get weights dictionary
    latest_prices = data.iloc[-1]  # Get latest prices
    allocations = {}

    for allocation_type, portfolio_class in allocation_classes.items():
        try:
            logger.info(
                f"Running {allocation_type} for Sr No={sr_no},total portfolio={total_rows} with budget={budget}...")
            portfolio = portfolio_class(weights, latest_prices, budget)
            allocation = portfolio.get_allocation()  # Get allocation
            allocations[allocation_type] = allocation
        except Exception as e:
            logger.error(f"Error in {allocation_type} for Sr No={sr_no}: {e}")
            allocations[allocation_type] = f"error at Sr No={sr_no}: {e}"
    return allocations


# Function to add allocation results to DataFrame
def add_post_processing_to_dataframe(results_df, post_processing):
    """
    Adds post_processing for each allocation type to the DataFrame.
    """
    for allocation_type, allocation_data in post_processing.items():
        # Log the lengths of allocation_data and results_df
        logger.info(f"allocation_data ==> {len(allocation_data)}, {len(results_df)}")

        # Add allocation data to the DataFrame using .loc to avoid SettingWithCopyWarning
        results_df.loc[:, f'Allocation_{allocation_type}_weight'] = allocation_data

        try:
            # Convert the allocation_data to a DataFrame (it should contain lists of [weights, remaining amount])
            allocation_df = pd.DataFrame(allocation_data, index=results_df.index)

            # Check if allocation_df has exactly 2 columns (for weights and remaining amount)
            if allocation_df.shape[1] != 2:
                logger.error(f"Allocation data for {allocation_type} does not have the expected 2 columns.")
                continue

            # Assign the two columns (weights and remaining amount) to the DataFrame
            results_df.loc[:, f'Allocation_{allocation_type}_weight'] = allocation_df.iloc[:,
                                                                        0]  # First column: weights
            results_df.loc[:, f'Allocation_{allocation_type}_remaining_amount'] = allocation_df.iloc[:,
                                                                                  1]  # Second column: remaining amount

        except Exception as e:
            logger.error(f"Error in getting allocation data for {allocation_type}: {e}")
            results_df.loc[:, f'Allocation_{allocation_type}_remaining_amount'] = f"error: {e}"


# Main function to process all rows
def run_all_post_processing_weight(results_df, data, current_month_dir, budget=1000000):
    """
    Processes all rows in the results DataFrame and adds post_processing to it.
    """
    total_rows = len(results_df)

    logger.info(f"Calculating processing_weight for the month {current_month_dir}")
    post_processing_weight_pkl_filepath = current_month_dir / PklFileConventions.post_processing_weight_pkl_filename

    post_processing = load_data_from_pickle(post_processing_weight_pkl_filepath)
    if post_processing is not None:
        return post_processing

    post_processing_classes = get_allocation_classes()
    post_processing = {alloc_type: [] for alloc_type in
                       post_processing_classes.keys()}  # Create a dict for each allocation type

    for sr_no, (index, row) in enumerate(results_df.iterrows(), start=1):
        row_post_processing = process_post_processing_for_row(sr_no, row, data, post_processing_classes, budget,
                                                              total_rows)
        for post_processing_type, allocation in row_post_processing.items():
            # Append to the correct list for the post_processing_type
            post_processing[post_processing_type].append(allocation)

    # Add allocation results to the DataFrame
    add_post_processing_to_dataframe(results_df, post_processing)
    save_data_to_pickle(post_processing_weight_pkl_filepath, results_df)
    logger.info("Processing weight completed successfully for the month {}".format(current_month_dir))
    return results_df
