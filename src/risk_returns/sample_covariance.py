# Derived class for Sample Covariance
from pypfopt import risk_models

from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.risk_returns.base_risk_model import BaseRiskModel


class SampleCovariance(BaseRiskModel):
    @ExecutionTimeRecorder(module_name=__name__)  # Use __name__ t
    def calculate_risk_matrix(self):
        return risk_models.risk_matrix(self.data, method="sample_cov")
