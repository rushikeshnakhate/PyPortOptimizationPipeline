# Data Downloader

This project provides a utility for downloading financial data from multiple sources, including Yahoo Finance, Alpha
Vantage, and Custom CSV files. The data downloader supports fetching data for various asset types such as stocks and
bonds, as well as for specific tickers. The functionality is encapsulated in the `get_data` function, which allows you
to specify the data source, asset type, tickers, and date range.

## Functionality

### `get_data`

The `get_data` function is the main entry point to fetch financial data for the specified tickers, date range, and data
source.

#### Parameters:

- `current_dir` (str): Current directory where the data will be saved/loaded from.
- `start_date` (str): Start date for data fetching in `YYYY-MM-DD` format.
- `end_date` (str): End date for data fetching in `YYYY-MM-DD` format.
- `tickers` (list, optional): List of tickers to fetch data for. If provided, it overrides configuration sources.
- `api_key` (str, optional): API key for data source (if required, e.g., for Alpha Vantage).
- `file_path` (str, optional): File path for Custom CSV source.
- `source_type` (str, default: `"YahooFinance"`): The source of the data (
  e.g., `YahooFinance`, `AlphaVantage`, `CustomCSV`).
- `asset_type` (str, default: `"stocks"`): The type of asset to fetch data for (e.g., `stocks`, `bonds`).

#### Returns:

- `pd.DataFrame`: A pandas `DataFrame` containing the combined data for the requested tickers or assets.

### How it Works:

1. **When Tickers are Provided**:
    - The function fetches data directly for the specified tickers using the corresponding downloader and asset type.
    - It calls the `get_downloader` function to retrieve the appropriate data downloader for the source type.
    - Then, it fetches the data for the specified tickers using the appropriate asset factory (`Stocks` or `Bonds`).

2. **When Tickers are Not Provided**:
    - The function loads the configuration using `load_config` to determine which sources and tickers to fetch.
    - For each source in the configuration, it retrieves the data by calling the appropriate downloader and asset
      factory, then combines all the fetched data into a single `DataFrame`.

### Example Usage:

```python
import os
import pandas as pd
from src.dataDownloader.main import get_data

# Specify parameters
current_dir = os.getcwd()
start_date = "2024-01-01"
end_date = "2024-01-31"
tickers = ["AAPL", "GOOGL"]
api_key = "your_alpha_vantage_api_key"

# Fetch data for the specified tickers
data = get_data(
    current_dir=current_dir,
    start_date=start_date,
    end_date=end_date,
    tickers=tickers,
    api_key=api_key,
    source_type="AlphaVantage",
    asset_type="stocks"
)

# Display fetched data
print(data.head())
