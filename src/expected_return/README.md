# PyExpectedReturns

A Python library for calculating expected returns using various statistical and financial models, including ARIMA, CAPM,
and Black-Litterman, to forecast asset performance based on historical dat

### Introduction

This code module provides functionalities for calculating various expected return metrics for financial assets. It
supports a wide range of methods, allowing you to explore diverse approaches to forecasting potential returns.

**Supported Expected Return Methods**

* **ARIMA (Autoregressive Integrated Moving Average):** Uses statistical modeling to predict future returns based on
  historical price patterns.
* **Arithmetic Mean Historical Return:** Calculates the average historical return of an asset.
* **Black-Litterman Model:** Combines historical data with subjective views to estimate expected returns.
* **Capital Asset Pricing Model (CAPM):** Estimates asset returns based on their market beta and risk-free rate.
* **CAGR Mean Historical Return:** Calculates the Compound Annual Growth Rate (CAGR) using historical returns.
* **Exponential Moving Average (EMA) Historical Return:** Uses an exponentially weighted average of past returns to
  estimate future returns.
* **Fama-French Model:** Estimates expected returns based on market, size, and value factors.
* **Gordon Growth Model:** Estimates the expected return of equities based on their dividend yield and expected growth
  rate.
* **Holt-Winters Model:** Combines exponential smoothing and seasonality forecasting to estimate future returns.
* **Linear Regression:** Estimates expected returns based on a linear relationship with independent variables (e.g.,
  market factors).
* **Risk Parity:** Allocates weights to assets based on their risk contribution to achieve a desired risk profile.
* **Time-Weighted Rate of Return (TWRR):** Calculates the annualized compound return accounting for cash flows within
  the period.

### Function
#### calculate_or_get_all_return
* This function calculates or retrieves all returns for a given dataset, based on the enabled methods specified. It can either calculate returns from scratch or fetch previously computed returns, depending on whether the data and enabled methods are provided.

#### Parameters:
* data (pd.DataFrame):
A pandas DataFrame containing the financial data for which returns need to be calculated.
Expected to include columns with price or value data for the assets being analyzed.
* current_dir (Path): The directory where the results or data related to the current month are stored. It is used for logging and may be involved in path resolution when saving or fetching results.
* enabled_methods (list, optional): A list of methods that should be used for calculating returns (e.g., "simple", "logarithmic").
If not provided, it will be loaded from a configuration file using the get_enabled_methods() function.
Defaults to None, in which case the method loads the enabled methods from the configuration.

#### Returns:
* pd.DataFrame: A DataFrame containing the calculated returns for the provided data. The structure of the returned DataFrame depends on the enabled methods and the calculations performed.


### Usage

1. Calling the calculate_all_returns Function
   To calculate expected returns using enabled methods, use the calculate_all_returns function. The function calculates
   all enabled return types and stores the results in a pickle file.

```python
from src.expected_return_calculator import calculate_all_returns

import pandas as pd
data = pd.DataFrame({
    'AAPL': [184.73, 183.35, 181.02, 180.29, 184.65],
    'GOOGL': [137.82, 138.57, 136.05, 135.39, 138.49]
}, index=pd.to_datetime([
    '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05', '2024-01-08'
]))
from pathlib import Path
output_dir = Path("path_to_output_directory")
enabled_methods = ['ARIMA', 'ArithmeticMeanHistorical']
df_returns = calculate_all_returns(data, output_dir, enabled_methods)
print(df_returns)
```


### How to Add New Methods?

To add a new return calculation method, follow these steps:
Create a New Class for the Return Type:

Create a new Python class for the method in the src/expected_return/ directory.
The class should implement a calculate_expected_return method that returns a DataFrame of expected returns.
Example:

```python
class NewReturnType:
    def __init__(self, data):
        self.data = data

    def calculate_expected_return(self, output_dir):
        # Calculate expected return and return as DataFrame
        return pd.DataFrame({
            'Ticker': ['AAPL', 'GOOGL'],
            'ExpectedReturn_NewMethod': [0.06, 0.04]
        }).set_index('Ticker')
```

### Update Configuration (Optional)
* If you want to control which methods are enabled from a configuration file, add the new method to the list of
enabled_methods in your configuration file (e.g., config.yaml).