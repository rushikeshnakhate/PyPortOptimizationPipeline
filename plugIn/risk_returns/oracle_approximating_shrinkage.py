# Derived class for Oracle Approximating Shrinkage
from pypfopt import risk_models

from plugIn.risk_returns.base_risk_model import BaseRiskModel


class OracleApproximatingShrinkage(BaseRiskModel):
    def calculate_risk_matrix(self):
        return risk_models.risk_matrix(self.data, method="oracle_approximating")
