from abc import ABC, abstractmethod

from pypfopt import DiscreteAllocation


class AllocationBase(ABC):
    def __init__(self, weights, latest_prices, total_portfolio_value=10000, short_ratio=None):
        self.weights = weights
        self.latest_prices = latest_prices
        self.total_portfolio_value = total_portfolio_value
        self.short_ratio = short_ratio

    @abstractmethod
    def get_allocation(self):
        pass


class GreedyPortfolio(AllocationBase):
    def __init__(self, weights, latest_prices, total_portfolio_value=10000, short_ratio=None):
        super().__init__(weights, latest_prices, total_portfolio_value, short_ratio)

    def get_allocation(self):
        self.discreteAllocation = DiscreteAllocation(
            self.weights,
            self.latest_prices,
            total_portfolio_value=self.total_portfolio_value,
            short_ratio=self.short_ratio
        )
        return self.discreteAllocation.greedy_portfolio()


class LpPortfolio(AllocationBase):
    def __init__(self, weights, latest_prices, total_portfolio_value=10000, short_ratio=None):
        super().__init__(weights, latest_prices, total_portfolio_value, short_ratio)

    def get_allocation(self):
        self.discreteAllocation = DiscreteAllocation(
            self.weights,
            self.latest_prices,
            total_portfolio_value=self.total_portfolio_value,
            short_ratio=self.short_ratio
        )
        return self.discreteAllocation.lp_portfolio()


class ProportionalGreedyPortfolio(AllocationBase):
    def __init__(self, weights, latest_prices, total_portfolio_value=10000, short_ratio=None):
        super().__init__(weights, latest_prices, total_portfolio_value, short_ratio)

    def get_allocation(self, reinvest=False, verbose=False):
        """
        Convert continuous weights into a discrete portfolio allocation
        using a proportional greedy approach.

        This method allocates proportionally to the weights at each iteration.
        It ensures that the number of shares bought is proportional to the current
        available funds at every step.

        :param reinvest: whether or not to reinvest cash gained from shorting
        :type reinvest: bool, defaults to False
        :param verbose: print error analysis?
        :type verbose: bool, defaults to False
        :return: the number of shares of each ticker that should be purchased,
                 along with the amount of funds leftover.
        :rtype: (dict, float)
        """
        # Sort in descending order of weight
        self.weights.sort(key=lambda x: x[1], reverse=True)

        available_funds = self.total_portfolio_value
        shares_bought = {ticker: 0 for ticker, weight in self.weights}

        # Allocate proportional to available funds
        while available_funds > 0:
            for ticker, weight in self.weights:
                price = self.latest_prices[ticker]
                proportion = weight * available_funds
                n_shares = int(proportion / price)
                cost = n_shares * price
                if cost <= available_funds:
                    shares_bought[ticker] += n_shares
                    available_funds -= cost
                if available_funds <= 0:
                    break

        self.allocation = self._remove_zero_positions(shares_bought)

        if verbose:
            print("Funds remaining: {:.2f}".format(available_funds))
            self._allocation_rmse_error(verbose)
        return self.allocation, available_funds


class MinRiskLpPortfolio(AllocationBase):
    def __init__(self, weights, latest_prices, total_portfolio_value=10000, short_ratio=None):
        super().__init__(weights, latest_prices, total_portfolio_value, short_ratio)

    def min_risk_lp_portfolio(self, reinvest=False, verbose=False, solver="ECOS_BB"):
        """
        Convert continuous weights into a discrete portfolio allocation
        by minimizing portfolio variance (risk) using linear programming.

        This method minimizes the portfolio risk subject to budget constraints.

        :param reinvest: whether or not to reinvest cash gained from shorting
        :type reinvest: bool, defaults to False
        :param verbose: print error analysis?
        :type verbose: bool, defaults to False
        :param solver: the CVXPY solver to use (must support mixed-integer programs)
        :type solver: str, defaults to "ECOS_BB"
        :return: the number of shares of each ticker that should be purchased,
                 along with the amount of funds leftover.
        :rtype: (dict, float)
        """
        p = self.latest_prices.values
        n = len(p)
        w = np.fromiter([i[1] for i in self.weights], dtype=float)

        # Assume covariance matrix is identity for now (can be modified later)
        cov_matrix = np.eye(n)

        # Integer allocation
        x = cp.Variable(n, integer=True)
        # Remaining dollars
        r = self.total_portfolio_value - p.T @ x

        # Minimize variance (risk) of the portfolio
        risk = cp.quad_form(x, cov_matrix)
        constraints = [x >= 0, r >= 0]  # long only constraints

        opt = cp.Problem(cp.Minimize(risk), constraints)
        opt.solve(solver=solver)

        if opt.status not in {"optimal", "optimal_inaccurate"}:
            raise ValueError("Linear program failed to find a solution.")

        self.allocation = self._remove_zero_positions(
            collections.OrderedDict(zip([i[0] for i in self.weights], x.value.astype(int)))
        )

        if verbose:
            print("Funds remaining: {:.2f}".format(r.value))
            self._allocation_rmse_error(verbose)
        return self.allocation, r.value
