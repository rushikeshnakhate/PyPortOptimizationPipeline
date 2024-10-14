# Derived class for Exponential Covariance
from pypfopt import risk_models

from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.risk_returns.base_risk_model import BaseRiskModel


class ExponentialCovariance(BaseRiskModel):
    @ExecutionTimeRecorder(module_name=__name__)  # Use __name__ t
    def calculate_risk_matrix(self):
        return risk_models.risk_matrix(self.data, method="exp_cov")
