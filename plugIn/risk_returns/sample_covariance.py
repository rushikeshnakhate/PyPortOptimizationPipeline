# Derived class for Sample Covariance
from pypfopt import risk_models

from plugIn.risk_returns.base_risk_model import BaseRiskModel


class SampleCovariance(BaseRiskModel):
    def calculate_risk_matrix(self):
        return risk_models.risk_matrix(self.data, method="sample_cov")
