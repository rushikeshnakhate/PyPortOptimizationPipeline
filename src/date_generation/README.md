# Date Range Generator Library

A Python library for generating date ranges based on specified years, months, and time frequencies. This library is designed for applications requiring automated date interval generation, such as time-series analysis, reporting, and scheduling.

---

## Features

- **Generate monthly or yearly date ranges**: Easily generate date intervals for either months or years.
- **Support for specific months within a year**: Allows specifying particular months to generate ranges for.
- **Accurate handling of leap years**: Automatically adjusts for leap years when generating date ranges for February.
- **Configurable frequency options**: Choose between `monthly` or `yearly` frequency when generating date ranges.
- **Easy to integrate**: Easily integrate into projects requiring date range generation with custom frequency definitions.

## Functions

### `generate_month_date_ranges`

Generates start and end date ranges for each month in a specified year.

#### Arguments:
- `year` (int): The year for which to generate the month ranges (e.g., `2024`).
- `months` (list of int, optional): A list of specific months to generate ranges for (1-12). Defaults to all months if not provided.

#### Returns:
- `list of tuples`: Each tuple contains a start date and end date for the specified month(s). The start and end dates are represented as `datetime.date` objects.

#### Example:

```python
generate_month_date_ranges(2024)
# Returns: [(datetime.date(2024, 1, 1), datetime.date(2024, 1, 31)), 
#           (datetime.date(2024, 2, 1), datetime.date(2024, 2, 29)), 
#           ...]
