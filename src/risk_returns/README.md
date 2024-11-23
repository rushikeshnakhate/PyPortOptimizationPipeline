### Portfolio Risk Calculator (PyRisksCalculator )

PyRisksCalculator is a Python library designed orchestrates the calculation of covariance matrices for multiple risk
models, loading them from pickle files if they exist, or calculating and saving them if they do not. This function is
part of the risk management pipeline and ensures that covariance matrices are available for further use in portfolio
optimization and risk management.

### Function

#### calculate_all_risk_matrix

#### Returns

* covariance_dict (dict):
  A dictionary where the keys are the names of the risk models (as strings), and the values are DataFrames representing
  the covariance matrices for each risk model.

#### Parameters

* data (pd.DataFrame):A DataFrame containing the financial data, such as asset returns, that will be used to compute the
  covariance matrices
  for the different risk models.

* output_dir (str):The directory where the computed covariance matrices will be saved as pickle files. If matrices
  already exist, they will
  be loaded from this directory.

#### Usage

````
# Example usage of calculate_all_risk_matrix

# Sample data (a DataFrame of asset returns)
import pandas as pd

# Assuming `data` is a DataFrame of asset returns
data = pd.DataFrame({
    'asset_1': [0.1, 0.2, 0.15, -0.1, 0.05],
    'asset_2': [0.05, 0.15, 0.2, -0.05, 0.1],
    'asset_3': [0.2, 0.3, 0.25, -0.1, 0.15]
})

# Output directory to save/load covariance matrices
output_dir = 'path_to_save_covariance_matrices'

# Call the function to calculate and return the covariance matrices for all enabled risk models
covariance_dict = calculate_all_risk_matrix(data, output_dir)

# Example of accessing the covariance matrix for a specific model
cov_matrix_sample_covariance = covariance_dict.get('SampleCovariance')

print(cov_matrix_sample_covariance)
````
