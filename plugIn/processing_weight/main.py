import logging

from tabulate import tabulate

from plugIn.processing_weight.greedy_portfolio import GreedyPortfolio

logger = logging.getLogger(__name__)


def run_all_post_processing_weight(results_df, data):
    allocations = []
    for index, row in results_df.iterrows():
        weights = row['Weights']  # Get the weights dictionary
        greedyPortfolio = GreedyPortfolio(weights, data.iloc[-1])
        allocation = greedyPortfolio.get_allocation()
        allocations.append(allocation)
    results_df['Allocation'] = allocations
    logger.info(tabulate(results_df, headers='keys', tablefmt='grid'))
