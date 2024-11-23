## PyOptimizers Library

PyOptimizers is a Python library designed to simplify portfolio optimization using various risk and return models. It
enables users to calculate efficient frontiers and obtain optimized portfolio weights with multiple optimization
methods.

## Introduction

* PyPortfolioOptFrontier
* PyPortfolioOptFrontierWithShortPosition
* MVRiskFolioOptimizer
* MADRiskFolioOptimizer
* MSVRiskFolioOptimizer
* FLPMRiskFolioOptimizer
* SLPMRiskFolioOptimizer
* CVaRRiskFolioOptimizer
* EVaRRiskFolioOptimizer
* WRRiskFolioOptimizer
* MDDRiskFolioOptimizer
* ADDRiskFolioOptimizer
* CDaRRiskFolioOptimizer
* UCIRiskFolioOptimizer
* EDaRRiskFolioOptimizer

## Usage

#### calculate_optimizations

This function calculates portfolio optimizations for all enabled methods, given expected returns and risk models.

#### Parameters:

* data (pd.DataFrame): Stock data to be optimized.
* expected_return_df (pd.DataFrame): Expected returns for various methods.
* risk_return_dict (dict): A dictionary containing covariance matrices for each risk model.
* current_month_dir (Path): Directory to store optimization outputs.
* enabled_methods (list, optional): Methods to use for optimization. Defaults to those specified in the configuration.

#### Returns:

* pd.DataFrame: A DataFrame with optimization results, including weights, expected annual returns, volatility, and
  Sharpe ratios.

### Usage:

```
from pathlib import Path
import pandas as pd
from pyoptimizers import calculate_optimizations

# Sample inputs
data = pd.DataFrame()  # Your stock data
expected_return_df = pd.DataFrame()  # Expected returns
risk_return_dict = {}  # Risk-return covariance matrices
current_month_dir = Path('./optimizations')  # Directory for storing results

# Call optimization function
optimized_data = calculate_optimizations(data, expected_return_df, risk_return_dict, current_month_dir)
print(optimized_data)
```

### How to Add New Methods?

* You can customize the library behavior by configuring the following parameters in the configuration file:
* Enabled Methods: Define which optimizers to use.
* Output Directory: Specify where results will be stored.

### Cache Management

* Loading from Cache: If an optimization result exists in the cache (*.pkl), the library automatically loads it to avoid
  redundant computations.
* Saving Results: Results are saved to pickle files for quick reuse.

