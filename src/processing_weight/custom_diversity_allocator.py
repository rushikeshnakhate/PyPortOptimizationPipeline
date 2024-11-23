import numpy as np
from src.processing_weight.allocationBase import AllocationBase


class CustomDiversityAllocator(AllocationBase):
    def __init__(self, weights, latest_prices, total_portfolio_value=100000, diversity_threshold=0.4):
        super().__init__(weights, latest_prices, total_portfolio_value)
        self.diversity_threshold = diversity_threshold

    def get_allocation(self):
        try:
            # Convert weights and prices from dicts to arrays
            tickers = list(self.weights.keys())
            weights_array = np.array([self.weights[ticker] for ticker in tickers])
            prices_array = np.array([self.latest_prices[ticker] for ticker in tickers])

            # Initial allocation based on weights and prices
            rounded_values = np.floor(weights_array * self.total_portfolio_value / prices_array).astype(int)

            # Calculate the allocation value for the asset with the highest weight
            allocation_values = rounded_values * prices_array
            max_allocation_value = np.max(allocation_values)
            max_threshold = self.total_portfolio_value * self.diversity_threshold

            # Adjust allocation if any asset exceeds the diversity threshold
            if max_allocation_value > max_threshold:
                # Redistribute funds to balance diversity
                avg_allocation_value = self.total_portfolio_value // len(tickers)
                allocation = np.minimum(
                    rounded_values,
                    np.floor(avg_allocation_value / prices_array).astype(int)
                )
                total_allocated_value = np.sum(allocation * prices_array)
                remaining_budget = self.total_portfolio_value - total_allocated_value

                # Redistribute the remaining budget
                for idx in np.argsort(weights_array)[::-1]:  # Start from the highest weight
                    if remaining_budget > 0:
                        max_shares_to_buy = remaining_budget // prices_array[idx]
                        allocation[idx] += max_shares_to_buy
                        remaining_budget -= max_shares_to_buy * prices_array[idx]
                    if remaining_budget <= 0:
                        break
            else:
                allocation = rounded_values
                remaining_budget = self.total_portfolio_value - np.sum(allocation * prices_array)

            # Convert allocation array back to a dictionary
            allocation_dict = {tickers[i]: allocation[i] for i in range(len(tickers))}
            return allocation_dict, remaining_budget

        except Exception as ex:
            return {"error": str(ex)}, 0
