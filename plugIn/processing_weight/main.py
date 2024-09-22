import logging
from tabulate import tabulate
from plugIn.processing_weight.greedy_portfolio import GreedyPortfolio
from plugIn.processing_weight.lp_portfolio import LpPortfolio
from plugIn.processing_weight.lp_portfolio import MinRiskLpPortfolio
from plugIn.processing_weight.pulp_portfolio import PulpPortfolio

logger = logging.getLogger(__name__)


def run_all_post_processing_weight(results_df, data):
    # Mapping allocation types to their corresponding classes
    allocation_classes = {
        'GreedyPortfolio': GreedyPortfolio,
        # 'ProportionalGreedyPortfolio': ProportionalGreedyPortfolio,
        'LpPortfolio': LpPortfolio,
        # 'PulpPortfolio': PulpPortfolio
        # 'MinRiskLpPortfolio': MinRiskLpPortfolio
    }

    allocations = {alloc_type: [] for alloc_type in allocation_classes.keys()}  # Create a dict for each allocation type

    for index, row in results_df.iterrows():
        weights = row['Weights']  # Get the weights dictionary
        latest_prices = data.iloc[-1]  # Get the latest prices

        for allocation_type, portfolio_class in allocation_classes.items():
            logger.info(f"Running {allocation_type}...")
            portfolio = portfolio_class(weights, latest_prices)
            allocation = portfolio.get_allocation()  # Get the allocation
            allocations[allocation_type].append(allocation)  # Append allocation to the corresponding list

    # Add allocations to the DataFrame for each allocation type
    logger.info("Results after post-processing:")
    for allocation_type in allocations:
        results_df[f'Allocation_{allocation_type}'] = allocations[allocation_type]

    logger.info(tabulate(results_df, headers='keys', tablefmt='grid'))
    return results_df

# Example usage
# run_all_post_processing_weight(results_df, data)
