import logging
import os
from pathlib import Path

import pandas as pd
from tabulate import tabulate
from plugIn.processing_weight.greedy_portfolio import GreedyPortfolio
from plugIn.processing_weight.lp_portfolio import LpPortfolio
from plugIn.processing_weight.lp_portfolio import MinRiskLpPortfolio

# from plugIn.processing_weight.pulp_portfolio import PulpPortfolio

logger = logging.getLogger(__name__)


def run_all_post_processing_weight(results_df, data, budget=1000000):
    # Mapping allocation types to their corresponding classes
    allocation_classes = {
        'GreedyPortfolio': GreedyPortfolio,
        # 'ProportionalGreedyPortfolio': ProportionalGreedyPortfolio,
        'LpPortfolio': LpPortfolio,
        # 'PulpPortfolio': PulpPortfolio
        # 'MinRiskLpPortfolio': MinRiskLpPortfolio
    }

    allocations = {alloc_type: [] for alloc_type in allocation_classes.keys()}  # Create a dict for each allocation type
    total_rows = len(results_df)  # Get the total number of rows
    for sr_no, (index, row) in enumerate(results_df.iterrows(), start=1):
        weights = row['Weights']  # Get the weights dictionary
        latest_prices = data.iloc[-1]  # Get the latest prices

        for allocation_type, portfolio_class in allocation_classes.items():
            logger.info(f"Running {allocation_type} for Sr No={sr_no}/{total_rows} with budget={budget}...")
            try:
                portfolio = portfolio_class(weights, latest_prices, budget)
                allocation = portfolio.get_allocation()  # Get the allocation
                allocations[allocation_type].append(allocation)  # Append allocation to the corresponding list
            except Exception as e:
                allocations[allocation_type].append(f"error at Sr No={sr_no}: {e}")

    # Add allocations to the DataFrame for each allocation type
    logger.info("Results after post-processing, extracting weights and remaining amounts in separate columns")
    for allocation_type in allocations:
        # allocation_data = allocations[allocation_type]
        try:
            results_df[f'Allocation_{allocation_type}_weight'] = allocations[allocation_type]
            results_df[[f'Allocation_{allocation_type}_weight',
                        f'Allocation_{allocation_type}_remaining_amount']] = pd.DataFrame(
                results_df[f'Allocation_{allocation_type}_weight'].tolist(), index=results_df.index)
        except Exception as e:
            results_df[[f'Allocation_{allocation_type}_weight',
                        f'Allocation_{allocation_type}_remaining_amount']] = f"error in getting: {e}"
    return results_df

# Example usage

# if __name__ == "__main__":
#     # Example usage
#     output_dir = Path(r"D:\PortfoliOpt\data")
#     data_pkl_filepath = os.path.join(output_dir, "data.pkl")
#     pkl_filepath = os.path.join(output_dir, "results.pkl")
#
#     results_df = pd.read_pickle(pkl_filepath)
#     data = pd.read_pickle(data_pkl_filepath)
#     results_df = run_all_post_processing_weight(results_df.head(4), data.head(4))
#     print(tabulate(results_df, headers='keys', tablefmt='grid'))
