# import pulp
import numpy as np

from plugIn.processing_weight.allocationBase import AllocationBase


class PulpPortfolio(AllocationBase):
    def __init__(self, weights, latest_prices, total_portfolio_value=100000, short_ratio=None):
        super().__init__(weights, latest_prices, total_portfolio_value, short_ratio)
        self.discreteAllocation = None

    def get_allocation(self):
        pass
        """
        Uses linear programming to convert continuous weights into an integer allocation of shares.
        """
        # Extract weight values from the dictionary (assuming weights is a dictionary)
        # weight_values = np.array(list(self.weights.values()))
        #
        # # Desired dollar allocations based on weights
        # desired_allocations = self.total_portfolio_value * weight_values
        #
        # # Initialize LP problem
        # problem = pulp.LpProblem("Portfolio Optimization", pulp.LpMinimize)
        #
        # # Variables: number of shares for each stock (integer)
        # n_shares = [pulp.LpVariable(f"shares_{i}", lowBound=0, cat='Integer') for i in range(len(self.latest_prices))]
        #
        # # Objective: Minimize the difference between desired and actual allocation (in dollar terms)
        # objective = pulp.lpSum(
        #     [abs(n_shares[i] * self.latest_prices[i] - desired_allocations[i]) for i in range(len(self.latest_prices))])
        # problem += objective
        #
        # # Constraint: The total value of purchased shares must not exceed the total portfolio value
        # problem += pulp.lpSum(
        #     [n_shares[i] * self.latest_prices[i] for i in range(len(self.latest_prices))]) <= self.total_portfolio_value
        #
        # # Solve the problem
        # problem.solve()
        #
        # # Store results in self.discreteAllocation
        # self.discreteAllocation = {f'Asset_{i}': int(n_shares[i].varValue) for i in range(len(n_shares))}
        # return self.discreteAllocation
