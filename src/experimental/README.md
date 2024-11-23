# Monte Carlo Simulation Library

This Python library provides a comprehensive implementation of Monte Carlo simulation for portfolio optimization. It
offers a flexible and efficient way to generate numerous random portfolio weight combinations and assess their
risk-return profiles.

## Introduction

- **Random Portfolio Generation**: Generates random portfolios with diverse weight distributions.
- **Risk and Return Calculation**: Computes expected return, volatility, and Sharpe ratio for each portfolio.
- **Optimal Portfolio Selection**: Identifies portfolios with maximum Sharpe ratio or minimum volatility.
- **Efficient Implementation**: Utilizes NumPy and Pandas for optimized calculations.
- **Flexible Configuration**: Allows customization of simulation parameters (number of portfolios, risk-free rate,
  etc.).

## Usage

### Prepare Data

```
from monte_carlo_simulation import MonteCarloSimulation
import pandas as pd

# Create a DataFrame with historical data
data = pd.DataFrame({
    "StockA": [0.01, 0.02, -0.01, 0.03],
    "StockB": [-0.02, 0.01, 0.04, 0.01],
    "StockC": [0.03, -0.01, 0.02, 0.05],
})
output_dir = "output_directory_path"
```

### run Simulation

```
monte_carlo_simulation = MonteCarloSimulation(data, output_dir)
max_sharpe_ratio, min_volatility = monte_carlo_simulation.run_monte_carlo_simulation()
```

