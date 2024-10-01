# Function to extract the dictionary from the string
import ast
from datetime import datetime, timedelta


def extract_dict_from_string(weight_str):
    # Split at the first space and take the second part
    dict_str = weight_str.split(' ', 1)[1]  # This removes the leading '0'
    # Split again to isolate the dictionary from the metadata
    dict_str = dict_str.split('Name:')[0].strip()  # Remove the metadata
    # Convert the string representation of the dictionary to an actual dictionary
    return dict_str


def clean_up(results_df):
    results_df['Weights'] = results_df['Weights'].astype(str)
    results_df['Weights'] = results_df['Weights'].apply(extract_dict_from_string)
    results_df['Weights'] = results_df['Weights'].apply(ast.literal_eval)


def generate_month_date_ranges(year):
    """Generate start_date and end_date (without time) for each month in the specified year."""
    month_ranges = []
    for month in range(1, 13):
        start_date = datetime(year, month, 1).date()  # Convert to date to remove time part
        if month == 12:
            end_date = (datetime(year + 1, 1, 1) - timedelta(days=1)).date()  # End of December, convert to date
        else:
            end_date = (datetime(year, month + 1, 1) - timedelta(
                days=1)).date()  # End of the current month, convert to date
        month_ranges.append((start_date, end_date))
    return month_ranges


def create_current_month_directory(start_date, output_dir):
    current_month = start_date.strftime("%Y%m")
    current_month_dir = output_dir / current_month
    current_month_dir.mkdir(parents=True, exist_ok=True)
    return current_month_dir
