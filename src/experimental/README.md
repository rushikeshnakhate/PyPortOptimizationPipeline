# Monte Carlo Simulation Library

This Python library provides a comprehensive implementation of Monte Carlo simulation for portfolio optimization. It
offers a flexible and efficient way to generate numerous random portfolio weight combinations and assess their
risk-return profiles.

## Key Features

- **Random Portfolio Generation**: Generates random portfolios with diverse weight distributions.
- **Risk and Return Calculation**: Computes expected return, volatility, and Sharpe ratio for each portfolio.
- **Optimal Portfolio Selection**: Identifies portfolios with maximum Sharpe ratio or minimum volatility.
- **Efficient Implementation**: Utilizes NumPy and Pandas for optimized calculations.
- **Flexible Configuration**: Allows customization of simulation parameters (number of portfolios, risk-free rate,
  etc.).




## Usage
```
from monte_carlo_simulation import MonteCarloSimulation
```

##  Prepare Your Data

1.  Create a pandas DataFrame with historical asset returns.
2.  Ensure the DataFrame has columns representing asset tickers and rows representing time periods.

```Example:

import pandas as pd

# Create a DataFrame with historical data
data = pd.DataFrame({
    "StockA": [0.01, 0.02, -0.01, 0.03],
    "StockB": [-0.02, 0.01, 0.04, 0.01],
    "StockC": [0.03, -0.01, 0.02, 0.05],
})
output_dir = "output_directory_path"
```

## run Simulation

```
simulation = MonteCarloSimulation(data, output_dir, num_of_portfolios=10000)
max_sharpe_portfolio, min_volatility_portfolio = simulation.run_monte_carlo_simulation()
import matplotlib.pyplot as plt

# Example to plot the portfolios
simulated_data = simulation.simulations_df
plt.scatter(simulated_data["Annual Volatility"], simulated_data["Expected Annual Return"], c=simulated_data["Sharpe Ratio"], cmap="viridis")
plt.colorbar(label="Sharpe Ratio")
plt.xlabel("Annual Volatility")
plt.ylabel("Expected Annual Return")
plt.title("Monte Carlo Simulation Efficient Frontier")
plt.show()
```