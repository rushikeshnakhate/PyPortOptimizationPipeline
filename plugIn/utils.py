# Function to extract the dictionary from the string
import ast
import logging
import os
import pickle

logger = logging.getLogger(__name__)
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


# Example usage:
# print(generate_month_date_ranges(2024))  # All months
# print(generate_month_date_ranges(2024, months=[1, 12]))  # January and December only


def create_current_month_directory(start_date, output_dir):
    current_month = start_date.strftime("%Y%m")
    current_month_dir = output_dir / current_month
    current_month_dir.mkdir(parents=True, exist_ok=True)
    return current_month_dir


def load_data_from_pickle(filepath):
    """
    Load optimization data from a pickle file.
    """
    if os.path.exists(filepath):
        logger.info(f"Loading optimization data from {filepath}")
        try:
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            logger.error(f"Error loading pickle file: {e}")
            return None
    return None


def save_data_to_pickle(filepath, data):
    """
    Save optimization data to a pickle file.
    """
    try:
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        logger.info(f" data saved to {filepath}")
    except Exception as e:
        logger.error(f"Error saving {filepath} data to pickle file: {e}")
