from datetime import datetime, timedelta

from src.common.conventions import GeneralConventions


def generate_month_date_ranges(year, months=None):
    """Generate start_date and end_date (without time) for each month in the specified year.

    Args:
        year (int): The year for which to generate the month ranges.
        months (list of int, optional): Specific months to generate ranges for (1-12).

    Returns:
        list of tuples: Each tuple contains the start and end date for the specified months.
    """
    if months is None:
        months = range(1, 13)  # Default to all months if none specified

    month_ranges = []
    for month in months:
        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = (datetime(year + 1, 1, 1) - timedelta(days=1)).date()
        else:
            end_date = (datetime(year, month + 1, 1) - timedelta(days=1)).date()
        month_ranges.append((start_date, end_date))

    return month_ranges


def generate_date_ranges(years: list, months=None, frequency=GeneralConventions.frequency_monthly):
    """Generate start_date and end_date ranges for specified years based on frequency.

    Args:
        years (list of int): List of years for which to generate the date ranges.
        months (list of int, optional): Specific months to generate ranges for (1-12).
        frequency (str): 'monthly' for monthly ranges or 'yearly' for a single range for each year.

    Returns:
        list of tuples: Each tuple contains the start and end date based on the specified frequency.
    """
    if not isinstance(years, (list, tuple)):
        raise ValueError("Years must be a list or tuple of integers.")

    all_date_ranges = []

    if frequency == GeneralConventions.frequency_multiyear:
        # For multi-year frequency, generate a start date and an end date for the entire range
        if len(years) < 2:
            raise ValueError("For multi-year frequency, the years list must contain at least two years.")
        # Sort the years to ensure correct start and end year
        years.sort()
        start_date = datetime(years[0], 1, 1).date()  # Start of the first year
        end_date = datetime(years[-1] + 1, 1, 1).date()  # Jan 1 of the year after the last year
        all_date_ranges.append((start_date, end_date))
        return all_date_ranges

    for year in years:
        if frequency == GeneralConventions.frequency_yearly:
            # Add a single tuple with the start and end date for the entire year
            start_date = datetime(year, 1, 1).date()
            end_date = datetime(year, 12, 31).date()
            all_date_ranges.append((start_date, end_date))
        elif frequency == GeneralConventions.frequency_monthly:
            # Add monthly ranges for the given year
            all_date_ranges.extend(generate_month_date_ranges(year, months))

        else:
            raise ValueError(f"Invalid frequency: {frequency}")

    return all_date_ranges
