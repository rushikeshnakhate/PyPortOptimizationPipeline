# Derived class for Ledoit-Wolf Constant Variance
from pypfopt import risk_models

from plugIn.risk_returns.base_risk_model import BaseRiskModel


class LedoitWolfConstantVariance(BaseRiskModel):
    def calculate_risk_matrix(self):
        return risk_models.risk_matrix(self.data, method="ledoit_wolf_constant_variance")