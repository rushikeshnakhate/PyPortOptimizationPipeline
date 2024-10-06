import logging

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


# Main function to process all rows
def run_all_post_processing_weight(results_df, data, current_month_dir, budget=1000000):
    """
    Processes all rows in the results DataFrame and adds post_processing to it, row-by-row, method-by-method.
    """
    total_rows = len(results_df)

    logger.info(f"Calculating processing_weight for the month {current_month_dir}")
    post_processing_weight_pkl_filepath = current_month_dir / PklFileConventions.post_processing_weight_pkl_filename
    post_processing = load_data_from_pickle(post_processing_weight_pkl_filepath)
    if post_processing is not None:
        return post_processing

    post_processing_classes = get_allocation_classes()

    for sr_no, (index, row) in enumerate(results_df.iterrows(), start=1):
        logger.info(f"Processing row {sr_no}/{total_rows}")

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

    save_data_to_pickle(post_processing_weight_pkl_filepath, results_df)
    logger.info("Processing weight completed successfully for the month {}".format(current_month_dir))
    return results_df
