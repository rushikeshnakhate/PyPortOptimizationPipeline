import os
import pickle
from abc import ABC, abstractmethod


# Base class for expected returns
class ExpectedReturnBase(ABC):
    def __init__(self, data):
        self.data = data
        self.cache_file = None

    @abstractmethod
    def calculate_expected_return(self):
        pass

    def _load_cache(self):
        """Load cached returns if available."""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'rb') as f:
                return pickle.load(f)
        return None

    def _save_cache(self, expected_returns):
        """Save expected returns to cache."""
        with open(self.cache_file, 'wb') as f:
            pickle.dump(expected_returns, f)
