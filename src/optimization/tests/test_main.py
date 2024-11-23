import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

from src.optimization.main import calculate_optimizations


class TestCalculateOptimizationsForRiskModel(unittest.TestCase):

    def test_calculate_optimizations_for_risk_model(self):
        expected_return_df = pd.DataFrame({"test": [0.1]})
        risk_return_dict = {"model1": np.array([[1]])}
        data = pd.DataFrame({"col1": [1]})
        current_month_dir = Path("test_dir")
        enabled_methods = ["method1"]

        result = calculate_optimizations(expected_return_df,
                                         risk_return_dict,
                                         data,
                                         current_month_dir,
                                         enabled_methods)

        # self.assertEqual(result.shape[0], 1)
        # self.assertEqual(result["test"].iloc[0], "result1")

        # # Assert that process_optimizer_results was called with expected arguments
        # mock_process_optimizer_results.assert_called_once_with(
        #     "test", "model1", expected_return_df["test"], risk_return_dict["model1"], data, current_month_dir,
        #     enabled_methods
        # )


if __name__ == '__main__':
    unittest.main()
