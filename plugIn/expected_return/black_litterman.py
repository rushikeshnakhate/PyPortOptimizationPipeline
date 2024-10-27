import numpy as np
import yfinance as yf

from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.expected_return.expected_returns_base import ExpectedReturnBase
from pypfopt import risk_models, BlackLittermanModel, black_litterman


class BlackLittermanReturn(ExpectedReturnBase):
    def __init__(self, data):
        super().__init__(data)
        self.delta = None
        self.mcaps = {}
        self.covariance_matrix = None
        self.data = data
        self.calculate_market_prior()
        self.market_prior = None  # This will be calculated dynamically
        self.investor_views = {'HDFCBANK.NS': 0.10}
        self.P_matrix = np.array([[1, -1, 0, 0], [0, 1, -1, 0]])  # Example P matrix
        # self.expected_returns = self.calculate_expected_return()

    def calculate_market_prior(self):
        tickers = self.data.columns

        for t in tickers:
            stock = yf.Ticker(t)
            self.mcaps[t] = stock.info["marketCap"]

        self.delta = black_litterman.market_implied_risk_aversion(self.data)
        self.covariance_matrix = risk_models.sample_cov(self.data)
        self.market_prior = black_litterman.market_implied_prior_returns(self.mcaps, self.delta, self.covariance_matrix)

    @ExecutionTimeRecorder(module_name=__name__)  # Use __name__ t
    def _calculate_expected_return(self):
        bl = BlackLittermanModel(self.covariance_matrix, self.market_prior, absolute_views=self.investor_views)
        self._convert_to_dataframe(bl.bl_returns())
