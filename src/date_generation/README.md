# Date Range Generator Library

A Python library for generating date ranges based on specified years, months, and time frequencies. This library is designed for applications requiring automated date interval generation, such as time-series analysis, reporting, and scheduling.

---

### Introduction

- **Generate monthly or yearly date ranges**: Easily generate date intervals for either months or years.
- **Support for specific months within a year**: Allows specifying particular months to generate ranges for.
- **Accurate handling of leap years**: Automatically adjusts for leap years when generating date ranges for February.
- **Configurable frequency options**: Choose between `monthly` or `yearly` frequency when generating date ranges.
- **Easy to integrate**: Easily integrate into projects requiring date range generation with custom frequency definitions.

### Function
#### `generate_month_date_ranges`
* Generates start and end date ranges for each month in a specified year.

#### Arguments:
* `year` (int): The year for which to generate the month ranges (e.g., `2024`).
* `months` (list of int, optional): A list of specific months to generate ranges for (1-12). Defaults to all months if not provided.
* `frequency`: frequency (str): 'monthly' for monthly ranges or 'yearly' for a single range for each year.
#### Returns:
- `list of tuples`: Each tuple contains a start date and end date for the specified month(s). The start and end dates are represented as `datetime.date` objects.

#### Usage:

```python
import datetime
from src.dataDownloader.main import generate_month_date_ranges

# Specify parameters
year = 2024
months = [1, 2, 3]  # Example of specific months

# Generate date ranges for the specified months
month_ranges = generate_month_date_ranges(year, months)

# Display the date ranges
for start_date, end_date in month_ranges:
    print(f"Start: {start_date}, End: {end_date}")
