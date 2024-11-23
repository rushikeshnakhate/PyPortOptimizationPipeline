# Derived class for PCA (Machine Learning-based risk model)
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.risk_returns.base_risk_model import BaseRiskModel


class PCARiskModel(BaseRiskModel):
    @ExecutionTimeRecorder(module_name=__name__)  # Use __name__ t
    def calculate_risk_matrix(self):
        pca = PCA(n_components=self.data.shape[1])
        pca.fit(self.data)
        covariance_matrix = np.cov(pca.components_)
        return pd.DataFrame(covariance_matrix, index=self.data.columns, columns=self.data.columns)
