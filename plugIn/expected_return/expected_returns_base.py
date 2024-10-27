import hashlib
import os
import pickle
from abc import ABC, abstractmethod

import pandas as pd

from plugIn.common.conventions import PklFileConventions, HeaderConventions


# Base class for expected returns
class ExpectedReturnBase(ABC):
    def __init__(self, data):
        self.data = data
        self.cache_file = None

    def _generate_cache_filename(self, output_dir):
        # Generate cache filename using the class name and a hash of the data characteristics
        class_name = self.__class__.__name__
        expected_return_pkl_filename = os.path.join(output_dir,
                                                    PklFileConventions.expected_return_pkl_filename.
                                                    format(expected_return_type=class_name))
        self.cache_file = os.path.join(output_dir, expected_return_pkl_filename)

    def _load_cache(self):
        # Load cached data if it exists
        if os.path.exists(self.cache_file):
            with open(self.cache_file, "rb") as f:
                print(f"Loading cached results from {self.cache_file}")
                return pickle.load(f)
        return None

    def _save_cache(self, result):
        # Save result to cache file
        with open(self.cache_file, "wb") as f:
            pickle.dump(result, f)
            print(f"Saved results to cache at {self.cache_file}")

    def calculate_expected_return(self, output_dir):
        # Check if cache exists
        self._generate_cache_filename(output_dir)
        cached_result = self._load_cache()
        if cached_result is not None:
            return cached_result

        # If no cache, calculate and cache the result
        result = self._calculate_expected_return()
        self._save_cache(result)
        return result

    def _convert_to_dataframe(self, expected_returns):
        """
        Converts a dictionary of expected returns to a DataFrame.
        :param expected_returns: Dictionary of expected returns {ticker: return}
        :return: DataFrame of expected returns with tickers as index
        """
        class_name = self.__class__.__name__
        expected_returns_df = pd.DataFrame(list(expected_returns.items()),
                                           columns=[HeaderConventions.ticker, class_name])
        expected_returns_df.set_index(HeaderConventions.ticker, inplace=True)
        return expected_returns_df

    @abstractmethod
    def _calculate_expected_return(self):
        pass
