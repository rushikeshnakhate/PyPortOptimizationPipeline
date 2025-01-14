from pydantic.dataclasses import dataclass


@dataclass
class PklFileConventions:
    post_processing_weight_pkl_filename: str = "post_processing_weight.pkl"
    performance_pkl_filename: str = "performance_metrics.pkl"
    expected_return_pkl_filename: str = "expected_return_{expected_return_type}.pkl"
    expected_return_for_all_type_pkl_filename: str = "expected_return_all_type.pkl"
    optimization_for_all_type_pkl_filename: str = "optimization_all_type.pkl"
    optimization_pkl_filename: str = "optimization_{optimization_type}_{expected_return_type}_{risk_return_type}.pkl"
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
    ticker: str = "ticker"


@dataclass
class GeneralConventions:
    frequency_yearly: str = "yearly"
    frequency_monthly: str = "monthly"
    frequency_multiyear: str = "multiyear"
