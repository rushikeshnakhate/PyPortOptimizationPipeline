# Graphical Lasso (Sparse Inverse Covariance) Risk Model
import pandas as pd
from sklearn.covariance import GraphicalLasso

from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.risk_returns.base_risk_model import BaseRiskModel


class GraphicalLassoRiskModel(BaseRiskModel):
    @ExecutionTimeRecorder(module_name=__name__)  # Use __name__ t
    def calculate_risk_matrix(self, alpha=0.01):
        model = GraphicalLasso(alpha=alpha)
        returns = self.data.pct_change().dropna()
        model.fit(returns)
        return pd.DataFrame(model.covariance_, index=self.data.columns, columns=self.data.columns)
