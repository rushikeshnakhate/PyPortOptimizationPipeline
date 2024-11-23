## Portfolio Performance Calculation Tool
This tool provides the functionality to calculate key performance metrics (such as Volatility, Return, and Sharpe Ratio) for portfolios based on allocation columns. It processes a post_processing_df DataFrame containing portfolio allocations, evaluates the performance using various metrics, and appends the results to the original DataFrame.

## Usage

####  calculate_performance
* The calculate_performance function calculates and appends performance metrics for portfolios based on allocation columns. It evaluates the performance of each portfolio using pre-defined metrics (Volatility, Return, Sharpe Ratio) and stores the results back into the provided post_processing_df.
* Loads existing performance data from a pickle file (if available).
* Iterates through the post_processing_df to extract portfolio allocation data.
* Converts the allocation data (in string format) to a dictionary for further processing.
* Calculates the portfolio's performance metrics using classes for PortfolioVolatility, PortfolioReturn, and PortfolioSharpeRatio.
* Appends the calculated metrics to the post_processing_df for each portfolio.
* Saves the updated post_processing_df to a pickle file for future use.

#### Parameters:
* post_processing_df (pd.DataFrame): The DataFrame that contains portfolio data with allocation columns. These allocations define how the portfolio is split across assets.
* data (dict or pd.DataFrame): Data used for calculating portfolio performance metrics. This could be stock price data or other asset data.
* start_date (str): The start date for performance calculation (in YYYY-MM-DD format).
* end_date (str): The end date for performance calculation (in YYYY-MM-DD format).
* current_month_dir (Path): The directory path where pickle files will be stored and loaded from. It is used to save and retrieve performance data for the current month.

#### Returns:
* post_processing_df (pd.DataFrame): The original post_processing_df with new columns for calculated performance metrics (Volatility, Return, Sharpe).
The new columns are named with the method name (e.g., Greedy_Volatility, Greedy_Return, Greedy_Sharpe).
```
import pandas as pd
from pathlib import Path
from mymodule.performance import calculate_performance

# Example post-processing DataFrame with allocation columns
post_processing_df = pd.DataFrame({
    'Allocation_Greedy': ["{'asset_1': 0.4, 'asset_2': 0.6}", "{'asset_1': 0.5, 'asset_2': 0.5}"],
    'Allocation_LP': ["{'asset_1': 0.3, 'asset_2': 0.7}", "{'asset_1': 0.6, 'asset_2': 0.4}"],
    'Greedy_remaining_amount': [1000, 1500],
    'LP_remaining_amount': [2000, 2500]
})

# Sample data (this could be price data or any asset data)
data = {
    'asset_1': [100, 105, 110, 108, 107],
    'asset_2': [200, 195, 193, 191, 190]
}

# Define start and end dates
start_date = "2024-01-01"
end_date = "2024-01-31"

# Define the directory for the current month
current_month_dir = Path("/path/to/data/2024-01")

# Call the function to calculate portfolio performance
updated_df = calculate_performance(post_processing_df, data, start_date, end_date, current_month_dir)

# Display the updated DataFrame with performance metrics
print(updated_df)
```