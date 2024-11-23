# Function to extract the dictionary from the string
import ast
import logging
import os
import pickle
from pathlib import Path

from src.common.conventions import GeneralConventions

logger = logging.getLogger(__name__)


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


def create_current_data_directory(start_date, end_date, output_dir, frequency=None):
    if frequency == GeneralConventions.frequency_yearly:
        current_dir_name = start_date.strftime("%Y")
    elif frequency == GeneralConventions.frequency_multiyear:
        start_year = start_date.strftime("%Y")
        end_year = end_date.strftime("%Y")
        current_dir_name = f"{start_year}_{end_year}"
    else:
        current_dir_name = start_date.strftime("%Y%m")
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
