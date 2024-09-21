from tkinter import Y

import numpy as np
import pandas as pd
from tabulate import tabulate


class EfficientFrontierBase:
    def __init__(self, expected_returns, covariance_matrix, data=None):
        self.expected_returns = expected_returns
        self.covariance_matrix = covariance_matrix
        self.cleaned_weights = None
        self.performance = None
        self.data = data

    def calculate_efficient_frontier(self):
        raise NotImplementedError("Subclasses should implement this method")

    def get_results(self):
        raise NotImplementedError("Subclasses should implement this method")
