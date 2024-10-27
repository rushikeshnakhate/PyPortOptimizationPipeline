from pathlib import Path

from pydantic.dataclasses import dataclass


@dataclass
class PklFileConventions:
    optimization_pkl_filename: str = "optimization.pkl"
    post_processing_weight_pkl_filename: str = "post_processing_weight.pkl"
    performance_pkl_filename: str = "performance.pkl"
    expected_return_pkl_filename: str = "expected_return.pkl"
    ending_pattern_for_risk_return_pkl_files: str = "covariance_{risk_return_type}.pkl"
    data_pkl_filename: str = "data.pkl"
    monte_carlo_pkl_filename: str = "monte_carlo_pkl_filename.pkl"
    short_listed_monte_carlo_pkl_filename: str = "short_listed_monte_pkl_filename.pkl"
    all_optimized_df_pkl_filename: str = "all_optimized_df.pkl"


@dataclass
class HeaderConventions:
    """
    Base dataclass for common headers across different stages.
    """
    expected_return_column: str = "Expected Return Type"
    risk_model_column: str = "Risk Model"
    annual_volatility_column: str = "Annual Volatility"
    sharpe_ratio_column: str = "Sharpe Ratio"
    expected_annual_return_column: str = "Expected Annual Return"
    weights_column: str = "Weights"
    optimizer_column: str = "Optimizer"
    cleaned_weights_column: str = "Cleaned Weights"
