import os
from abc import ABC, abstractmethod

import pandas as pd

from src.common.conventions import PklFileConventions, HeaderConventions
from src.common.utils import load_data_from_pickle, save_data_to_pickle


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

    def calculate_expected_return(self, output_dir):
        # Check if cache exists
        self._generate_cache_filename(output_dir)
        cached_result = load_data_from_pickle(self.cache_file)
        if cached_result is not None:
            return cached_result

        # If no cache, calculate and cache the result
        result = self._calculate_expected_return()
        save_data_to_pickle({self.cache_file}, result)
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
