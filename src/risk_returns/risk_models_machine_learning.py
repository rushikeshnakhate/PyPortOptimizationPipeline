from arch import arch_model  # For GARCH models
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR

from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.risk_returns.base_risk_model import BaseRiskModel


# Autoencoders for Covariance Estimation
# class AutoencoderRiskModel(BaseRiskModel):
#     def calculate_risk_matrix(self):
#         returns = self.data.pct_change().dropna()
#         model = self.build_autoencoder(input_dim=returns.shape[1])
#         model.fit(returns.values, returns.values, epochs=100, batch_size=32, verbose=0)
#         compressed_data = model.predict(returns.values)
#         cov_matrix = np.cov(compressed_data.T)
#         return pd.DataFrame(cov_matrix, index=self.data.columns, columns=self.data.columns)
#
#     def build_autoencoder(self, input_dim):
#         model = models.Sequential()
#         model.add(layers.InputLayer(input_shape=(input_dim,)))
#         model.add(layers.Dense(32, activation='relu'))
#         model.add(layers.Dense(16, activation='relu'))
#         model.add(layers.Dense(32, activation='relu'))
#         model.add(layers.Dense(input_dim, activation='linear'))
#         model.compile(optimizer='adam', loss='mse')
#         return model


# Random Forest Volatility Prediction
class RandomForestVolatility(BaseRiskModel):
    @ExecutionTimeRecorder(module_name=__name__)  # Use __name__ t
    def calculate_risk_matrix(self):
        # Compute percentage change in data (returns) and remove NaN values
        X = self.data.pct_change().dropna()

        # Calculate the standard deviation of each row (volatility)
        y = X.std(axis=1)

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Train the Random Forest model
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)

        # Predict the volatility (standard deviation) for the test set
        y_pred = rf_model.predict(X_test)

        # Create a covariance matrix with the predicted volatilities on the diagonal
        diag_volatility = np.diag(y_pred)

        # Convert the diagonal matrix into a pandas DataFrame
        # Filling off-diagonal elements with 0, the index and columns should be the same as in the original data
        # Since this is volatility for individual assets, we assume a diagonal covariance matrix
        asset_count = len(self.data.columns)  # Number of assets
        covariance_matrix = np.zeros((asset_count, asset_count))  # Initialize a zero matrix
        np.fill_diagonal(covariance_matrix, y_pred[:asset_count])  # Fill the diagonal with predicted volatilities

        # Create a DataFrame, ensuring the index and columns match the assets in the original data
        return pd.DataFrame(covariance_matrix, index=self.data.columns, columns=self.data.columns)


# Gaussian Processes for Risk Estimation
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF


class GaussianProcessRiskModel(BaseRiskModel):
    def calculate_risk_matrix(self):
        # Compute percentage change in data (returns) and remove NaN values
        X = self.data.pct_change().dropna()

        # Calculate the standard deviation of each row (volatility)
        y = X.std(axis=1)

        # Initialize a Gaussian Process Regressor with an RBF kernel
        gp = GaussianProcessRegressor(kernel=RBF(), random_state=42)

        # Fit the Gaussian Process model
        gp.fit(X, y)

        # Predict standard deviation (sigma) using the Gaussian Process
        y_pred, sigma = gp.predict(X, return_std=True)

        # Create a covariance matrix with the predicted volatilities (sigma) on the diagonal
        diag_volatility = np.diag(sigma)

        # Convert the diagonal matrix into a pandas DataFrame
        # Filling off-diagonal elements with 0, the index and columns should be the same as in the original data
        asset_count = len(self.data.columns)  # Number of assets
        covariance_matrix = np.zeros((asset_count, asset_count))  # Initialize a zero matrix
        np.fill_diagonal(covariance_matrix, sigma[:asset_count])  # Fill diagonal with predicted standard deviations

        # Create a DataFrame, ensuring the index and columns match the assets in the original data
        return pd.DataFrame(covariance_matrix, index=self.data.columns, columns=self.data.columns)


# Bayesian Networks
import pgmpy.models as pgm
from pgmpy.estimators import MaximumLikelihoodEstimator


# Support Vector Machines (SVM) for Volatility Prediction
class SVMVolatility(BaseRiskModel):
    def calculate_risk_matrix(self):
        # Compute percentage change in data (returns) and remove NaN values
        X = self.data.pct_change().dropna()

        # Compute the volatility (standard deviation) for each asset over time (for each column)
        y = X.std(axis=0)  # Axis 0 for columns (assets)

        # Initialize an SVR model with an RBF kernel
        svr = SVR(kernel='rbf')

        # Fit the SVR model using each column (asset's returns) as a feature and its volatility as the target
        svr.fit(np.arange(len(y)).reshape(-1, 1), y)

        # Predict volatilities for each asset
        y_pred = svr.predict(np.arange(len(y)).reshape(-1, 1))

        # Create a volatility matrix (diagonal matrix with predicted volatilities)
        volatility_matrix = np.diag(y_pred)

        # Convert the volatility matrix to a pandas DataFrame, matching the shape of the asset names
        return pd.DataFrame(volatility_matrix, index=self.data.columns, columns=self.data.columns)


# Clustering Techniques (e.g., K-Means)
class KMeansClustering(BaseRiskModel):
    def calculate_risk_matrix(self):
        # Compute percentage change in data (returns) and remove NaN values
        returns = self.data.pct_change().dropna()

        # Apply KMeans clustering to the returns data
        kmeans = KMeans(n_clusters=2, random_state=42)
        kmeans.fit(returns)

        # Get the labels for each cluster (though we don't need them for covariance calculation here)
        clusters = kmeans.labels_

        # Calculate the covariance matrix of the returns
        covariance_matrix = np.cov(returns.T)

        # Convert the covariance matrix to a pandas DataFrame with asset names as index and columns
        return pd.DataFrame(covariance_matrix, index=self.data.columns, columns=self.data.columns)


# GARCH Model

# Copula Models for Multivariate Risk


class CopulaRiskModel(BaseRiskModel):
    def calculate_risk_matrix(self):
        # Compute percentage change in data (returns) and remove NaN values
        returns = self.data.pct_change().dropna()

        # Initialize and fit the Gaussian Mixture Model
        copula_model = GaussianMixture(n_components=2)
        copula_model.fit(returns)

        # Retrieve the covariance matrices from the GMM
        covariances = copula_model.covariances_

        # Average the covariance matrices across components
        # This step assumes the covariance matrices are compatible for averaging
        avg_covariance = np.mean(covariances, axis=0)

        # Convert the covariance matrix to a pandas DataFrame
        return pd.DataFrame(avg_covariance, index=self.data.columns, columns=self.data.columns)


# Regime-Switching Model
from sklearn.mixture import GaussianMixture
import numpy as np
import pandas as pd


class RegimeSwitchingRiskModel(BaseRiskModel):
    def calculate_risk_matrix(self):
        # Compute percentage change in data (returns) and remove NaN values
        returns = self.data.pct_change().dropna()

        # Initialize and fit the Gaussian Mixture Model
        model = GaussianMixture(n_components=2)
        model.fit(returns)

        # Retrieve the covariance matrices from the GMM
        cov_matrices = model.covariances_

        # Average the covariance matrices between regimes
        avg_covariance = np.mean(cov_matrices, axis=0)

        # Convert the covariance matrix to a pandas DataFrame
        return pd.DataFrame(avg_covariance, index=self.data.columns, columns=self.data.columns)


# TO DO - NOT IMPLEMENTED
class BayesianNetworkRiskModel(BaseRiskModel):
    def calculate_risk_matrix(self):
        returns = self.data.pct_change().dropna()
        model = pgm.BayesianModel()
        model.fit(returns, estimator=MaximumLikelihoodEstimator)
        # Returns adjacency matrix of Bayesian Network, which can be converted into covariance estimates
        return model


class GARCHRiskModel(BaseRiskModel):
    def calculate_risk_matrix(self):
        returns = self.data.pct_change().dropna()
        cov_matrix = []
        for ticker in returns.columns:
            model = arch_model(returns[ticker], vol='Garch', p=1, q=1)
            res = model.fit(disp="off")
            cov_matrix.append(res.conditional_volatility)
        return np.diag(np.mean(cov_matrix, axis=0))


# Neural Networks for Volatility Prediction
class NeuralNetworkVolatility(BaseRiskModel):
    def calculate_risk_matrix(self):
        X = self.data.pct_change().dropna()
        y = X.std(axis=1)
        nn_model = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=500, random_state=42)
        nn_model.fit(X, y)
        y_pred = nn_model.predict(X)
        return np.diag(y_pred)
