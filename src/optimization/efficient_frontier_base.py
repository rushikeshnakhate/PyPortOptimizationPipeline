import os
import pickle

from src.common.conventions import PklFileConventions
from src.common.utils import load_data_from_pickle, save_data_to_pickle


class EfficientFrontierBase:
    def __init__(self, expected_returns, covariance_matrix, expected_return_type, risk_return_type,
                 output_dir=None,
                 data=None):
        self.expected_returns = expected_returns
        self.covariance_matrix = covariance_matrix
        self.cleaned_weights = None
        self.performance = None
        self.data = data
        self.cache_file = self._generate_cache_filename(output_dir=output_dir,
                                                        expected_return_type=expected_return_type,
                                                        risk_return_type=risk_return_type)

    def _generate_cache_filename(self, output_dir, expected_return_type, risk_return_type):
        # Generate cache filename using the class name and a hash of the data characteristics
        class_name = self.__class__.__name__
        expected_return_pkl_filename = os.path.join(output_dir,
                                                    PklFileConventions.optimization_pkl_filename.
                                                    format(expected_return_type=expected_return_type,
                                                           risk_return_type=risk_return_type,
                                                           optimization_type=class_name))
        return os.path.join(output_dir, expected_return_pkl_filename)

    def get_results(self):
        cached_result = load_data_from_pickle(self.cache_file)
        if cached_result is None:
            df = self._get_results()
            save_data_to_pickle(pkl_filename=self.cache_file, dataframe=df)
            cached_result = df
        return cached_result

    def calculate_efficient_frontier(self):
        raise NotImplementedError("Subclasses should implement this method")

    def _get_results(self):
        raise NotImplementedError("Subclasses should implement this method")
