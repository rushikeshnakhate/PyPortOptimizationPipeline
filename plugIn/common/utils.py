# Function to extract the dictionary from the string
import ast
import logging
import os
import pickle
from pathlib import Path

from plugIn.common.conventions import GeneralConventions

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

def generate_date_ranges(year, months=None, frequency=GeneralConventions.frequency_monthly):
    """Generate start_date and end_date ranges for each month or the entire year based on frequency.

    Args:
        year (int): The year for which to generate the date ranges.
        months (list of int, optional): Specific months to generate ranges for (1-12).
        frequency (str): 'monthly' for monthly ranges or 'yearly' for a single range for the entire year.

    Returns:
        list of tuples: Each tuple contains the start and end date based on the specified frequency.
    """
    if frequency == GeneralConventions.frequency_yearly:
        # Return a single tuple with the start and end date for the entire year
        start_date = datetime(year, 1, 1).date()
        end_date = datetime(year, 12, 31).date()
        return [(start_date, end_date)]
    return generate_month_date_ranges(year, months)


def create_current_data_directory(start_date, output_dir, frequency=None):
    current_dir_name = start_date.strftime("%Y%m")
    if frequency == GeneralConventions.frequency_yearly:
        current_dir_name = start_date.strftime("%Y")
    current_dir_with_path = Path(output_dir) / current_dir_name
    current_dir_with_path.mkdir(parents=True, exist_ok=True)
    return current_dir_with_path


def load_data_from_pickle(pkl_filename):
    """
    Load optimization data from a pickle file.
    """
    if os.path.exists(pkl_filename):
        logger.info(f"Loading data from pkl file=`{pkl_filename}`")
        try:
            with open(pkl_filename, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            logger.error(f"Error={e} while loading pickle file={pkl_filename}")
            return None
    return None


def save_data_to_pickle(pkl_filename, dataframe):
    """
    Save optimization data to a pickle file.
    """
    try:
        with open(pkl_filename, 'wb') as f:
            pickle.dump(dataframe, f)
        logger.info(f" data saved to filepath={pkl_filename}")
    except Exception as e:
        logger.error(f"Error={e} saving data to pickle file={pkl_filename}")
