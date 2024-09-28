from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
from pypfopt import risk_models
from sklearn.covariance import GraphicalLasso
from sklearn.decomposition import PCA


# from tensorflow.keras import layers, models
# Bayesian Networks
# import pgmpy.models as pgm
# from pgmpy.estimators import MaximumLikelihoodEstimator


# Base class for Risk Models
class BaseRiskModel(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def calculate_risk_matrix(self):
        pass


# Derived class for Sample Covariance
class SampleCovariance(BaseRiskModel):
    def calculate_risk_matrix(self):
        return risk_models.risk_matrix(self.data, method="sample_cov")


# Derived class for Semi-Covariance
class SemiCovariance(BaseRiskModel):
    def calculate_risk_matrix(self):
        return risk_models.risk_matrix(self.data, method="semicovariance")


# Derived class for Exponential Covariance
class ExponentialCovariance(BaseRiskModel):
    def calculate_risk_matrix(self):
        return risk_models.risk_matrix(self.data, method="exp_cov")


# Derived class for Ledoit-Wolf Shrinkage
class LedoitWolfShrinkage(BaseRiskModel):
    def calculate_risk_matrix(self):
        return risk_models.risk_matrix(self.data, method="ledoit_wolf")


# Derived class for Ledoit-Wolf Constant Variance
class LedoitWolfConstantVariance(BaseRiskModel):
    def calculate_risk_matrix(self):
        return risk_models.risk_matrix(self.data, method="ledoit_wolf_constant_variance")


# Derived class for Ledoit-Wolf Single Factor
class LedoitWolfSingleFactor(BaseRiskModel):
    def calculate_risk_matrix(self):
        return risk_models.risk_matrix(self.data, method="ledoit_wolf_single_factor")


# Derived class for Ledoit-Wolf Constant Correlation
class LedoitWolfConstantCorrelation(BaseRiskModel):
    def calculate_risk_matrix(self):
        return risk_models.risk_matrix(self.data, method="ledoit_wolf_constant_correlation")


# Derived class for Oracle Approximating Shrinkage
class OracleApproximatingShrinkage(BaseRiskModel):
    def calculate_risk_matrix(self):
        return risk_models.risk_matrix(self.data, method="oracle_approximating")


# Derived class for PCA (Machine Learning-based risk model)
class PCARiskModel(BaseRiskModel):
    def calculate_risk_matrix(self):
        pca = PCA(n_components=self.data.shape[1])
        pca.fit(self.data)
        covariance_matrix = np.cov(pca.components_)
        return pd.DataFrame(covariance_matrix, index=self.data.columns, columns=self.data.columns)


# Graphical Lasso (Sparse Inverse Covariance) Risk Model
class GraphicalLassoRiskModel(BaseRiskModel):
    def calculate_risk_matrix(self, alpha=0.01):
        model = GraphicalLasso(alpha=alpha)
        returns = self.data.pct_change().dropna()
        model.fit(returns)
        return pd.DataFrame(model.covariance_, index=self.data.columns, columns=self.data.columns)
