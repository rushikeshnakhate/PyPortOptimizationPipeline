import pandas as pd
from tabulate import tabulate

from plugIn.expected_return.expected_returns import CAGRMeanHistoricalReturn, ArithmeticMeanHistoricalReturn, \
    EMAHistoricalReturn, CAPMReturn
from plugIn.expected_return.expected_returns_black_litterman import BlackLittermanReturn
from plugIn.expected_return.expected_returns_fama_french import FamaFrenchReturn
from plugIn.expected_return.expected_returns_gordon_growth import GordonGrowthReturn
from plugIn.expected_return.expected_returns_machine_learning_arima import ARIMAReturn
from plugIn.expected_return.expected_returns_machine_learning_linearRegression import LinearRegressionReturn
from plugIn.expected_return.expected_returns_risk_parity import RiskParityReturn
from plugIn.get_stocks import get_stocks


def update_returns_dataframe(df_returns, return_type, return_values):
    return_series = pd.Series(return_values, name=return_type)
    return df_returns.join(return_series, how='outer')


def calculate_all_returns(data):
    """Calculate all the different returns (mean, ema, capm, etc.) using a loop."""
    # Create a mapping of return types to their respective classes
    return_calculators = {
        'CAGRMeanHistorical': CAGRMeanHistoricalReturn(data),
        'ArithmeticMeanHistorical': ArithmeticMeanHistoricalReturn(data),
        'EMAHistorical': EMAHistoricalReturn(data),
        'CAPM': CAPMReturn(data),
        # 'TWRR': TWRRReturn(data),
        'GordonGrowth': GordonGrowthReturn(data),
        'FamaFrench': FamaFrenchReturn(data),
        'LinearRegression': LinearRegressionReturn(data),
        'RiskParity': RiskParityReturn(data),
        'BlackLitterman': BlackLittermanReturn(data),
        # 'HoltWinters': HoltWintersReturn(data),
        'ARIMA': ARIMAReturn(data)
    }

    # Initialize an empty DataFrame to store returns
    df_returns = pd.DataFrame()

    # Loop through each return type and add to the DataFrame
    for return_type, calculator in return_calculators.items():
        return_values = calculator.calculate_expected_return()
        df_returns = update_returns_dataframe(df_returns, return_type, return_values)

    return df_returns

# if __name__ == "__main__":
#     data = get_stocks()
#     expected_return_df = calculate_all_returns(data)
#     print(tabulate(expected_return_df, headers='keys', tablefmt='grid'))
