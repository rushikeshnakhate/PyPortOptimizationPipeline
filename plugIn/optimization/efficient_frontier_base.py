import os
import pickle

from plugIn.common.conventions import PklFileConventions


class EfficientFrontierBase:
    def __init__(self, expected_returns, covariance_matrix, data=None):
        self.expected_returns = expected_returns
        self.covariance_matrix = covariance_matrix
        self.cleaned_weights = None
        self.performance = None
        self.data = data
        self.cache_file = None

    def _generate_cache_filename(self, output_dir):
        # Generate cache filename using the class name and a hash of the data characteristics
        class_name = self.__class__.__name__
        expected_return_pkl_filename = os.path.join(output_dir,
                                                    PklFileConventions.optimization_pkl_filename.
                                                    format(optimization_type=class_name))
        self.cache_file = os.path.join(output_dir, expected_return_pkl_filename)

    def _load_cache(self, output_dir):
        self._generate_cache_filename(output_dir)
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

    def get_results(self, output_dir):
        cached_result = self._load_cache(output_dir)
        if cached_result is not None:
            df = self._get_results()
            self._save_cache(df)
        return cached_result

    def calculate_efficient_frontier(self):
        raise NotImplementedError("Subclasses should implement this method")

    def _get_results(self):
        raise NotImplementedError("Subclasses should implement this method")
