### Portfolio Allocation Processor (PyPAP)

The Portfolio Allocation Processor (PyPAP) is a Python library designed to process and allocate portfolio weights based
on
different allocation methods. It supports multiple portfolio classes, calculates weights and remaining amounts, and
provides functionality to extend the system with new allocation methods. This library can be used in financial and
investment analysis, portfolio optimization, and asset allocation.

#### Introduction

* CustomClusteredAllocator: A custom-designed allocator that optimizes asset allocation based on clustering techniques,
  improving risk diversification.
* CustomDiversityAllocator: A custom-designed allocator that ensures optimal diversification by balancing assets across
  different risk profiles.
* CustomProportionalRoundingAllocator: A custom-designed allocator that adjusts portfolio weights proportionally while
  maintaining rounding constraints for practical implementation.
* CustomTransactionCostAllocator: A custom-designed allocator that accounts for transaction costs in the asset
  allocation
  process, optimizing for net returns after costs.
* CustomWeightedFloorAllocator: A custom-designed allocator that applies weight floors to ensure minimum allocations
  while
  optimizing for returns and risk.
* GreedyPortfolio: A portfolio that sequentially selects the best assets based on a greedy algorithm to maximize
  returns.
* LpPortfolio: A portfolio allocation model that optimizes based on linear programming techniques, balancing returns and
  risk efficiently.

### Function

#### run_all_post_processing_weight

#### Returns

* a dictionary of allocation classes that are enabled based on the enabled_methods parameter. If
  no methods are specified, it returns all available classes.

#### Parameters

* results_df (pd.DataFrame): A DataFrame containing the portfolio data that needs processing. This will include weights
  and other necessary data for allocation.
* data (pd.DataFrame): A DataFrame containing market data, which could include prices, market indices, etc., for the
  calculation of portfolio allocations.
* current_month_dir (Path): The directory path for storing the results of the processing for the current month.
* enabled_methods (list, optional): A list of allocation methods (e.g., GreedyPortfolio, LpPortfolio). If not provided,
  the function loads enabled methods from the configuration.
* budget (int, optional): The total budget available for allocation. The default value is 1,000,000.

#### Usage

1. Importing the necessary libraries and setting up data:

````
import pandas as pd
from pathlib import Path
from src.processing_weight import PortfolioAllocationProcessor as PAP

# Sample data: Assume that `results_df` and `data` are already loaded or generated
results_df = pd.DataFrame({
    'weights_column': [{'stock_a': 0.5, 'stock_b': 0.3, 'stock_c': 0.2}],
    'other_column': ['data']
})

data = pd.DataFrame({
    'stock_a': [100, 105, 110],
    'stock_b': [200, 210, 215],
    'stock_c': [150, 145, 140]
})

# Path to the current month's directory where the results will be saved
current_month_dir = Path("/path/to/current_month_dir")
````

2. Running the allocation processing:

```
# If you want to use specific enabled methods:
enabled_methods = ['GreedyPortfolio', 'LpPortfolio']

# Or, if you want to let the function load enabled methods from the config file:
enabled_methods = None  # The function will load enabled methods from config

# Run the function to process the portfolio data and allocation
final_results_df = PAP.run_all_post_processing_weight(
    results_df=results_df, 
    data=data, 
    current_month_dir=current_month_dir, 
    enabled_methods=enabled_methods, 
    budget=1000000
)
```

