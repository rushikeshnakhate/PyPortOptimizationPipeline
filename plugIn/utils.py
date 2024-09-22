# Function to extract the dictionary from the string
import ast


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
