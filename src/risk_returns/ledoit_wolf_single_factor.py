# Derived class for Ledoit-Wolf Single Factor
from pypfopt import risk_models

from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.risk_returns.base_risk_model import BaseRiskModel


class LedoitWolfSingleFactor(BaseRiskModel):
    @ExecutionTimeRecorder(module_name=__name__)  # Use __name__ t
    def calculate_risk_matrix(self):
        return risk_models.risk_matrix(self.data, method="ledoit_wolf_single_factor")
