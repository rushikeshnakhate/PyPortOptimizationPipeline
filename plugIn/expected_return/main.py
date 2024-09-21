import pandas as pd

from plugIn.expected_return.expected_returns import CAPMReturn, ArithmeticMeanHistoricalReturn, \
    CAGRMeanHistoricalReturn, EMAHistoricalReturn
from plugIn.expected_return.expected_returns_black_litterman import BlackLittermanReturn
from plugIn.expected_return.expected_returns_fama_french import FamaFrenchReturn
from plugIn.expected_return.expected_returns_gordon_growth import GordonGrowthReturn
from plugIn.expected_return.expected_returns_machine_learning_arima import ARIMAReturn
from plugIn.expected_return.expected_returns_machine_learning_linearRegression import LinearRegressionReturn
from plugIn.expected_return.expected_returns_risk_parity import RiskParityReturn
from plugIn.expected_return.monte_carlo_simulation import MonteCarloSimulation
from plugIn.get_stocks import get_stocks


def run_monte_carlo_simulation(data):
    """Run the Monte Carlo Simulation and return max Sharpe ratio and min volatility portfolios."""
    monte_carlo_simulation = MonteCarloSimulation(data.columns, data)
    monte_carlo_simulation.run_simulation()

    # Retrieve results for max Sharpe Ratio and min Volatility portfolios
    max_sharpe_ratio = monte_carlo_simulation.get_max_sharpe_ratio()
    min_volatility = monte_carlo_simulation.get_min_volatility()

    return max_sharpe_ratio, min_volatility


def update_returns_dataframe(df_returns, return_type, return_values):
    """
    Adds the new return type (max Sharpe, min Volatility, etc.) to the DataFrame.

    :param df_returns: DataFrame containing all the return values.
    :param return_type: The type of return being added (e.g., 'Max Sharpe Ratio', 'Mean Historical Return').
    :param return_values: A dictionary of returns (e.g., {'AAPL': 0.10, 'GOOGL': 0.12}).
    """
    return_series = pd.Series(return_values, name=return_type)
    return df_returns.join(return_series, how='outer')


def calculate_all_returns(data):
    """Calculate all the different returns (mean, ema, capm, etc.) using a loop."""
    # Create a mapping of return types to their respective classes
    return_calculators = {
        'CAGRMeanHistorical': CAGRMeanHistoricalReturn(data),
        # 'ArithmeticMeanHistorical': ArithmeticMeanHistoricalReturn(data),
        # 'EMAHistorical': EMAHistoricalReturn(data),
        # 'CAPM': CAPMReturn(data),
        # # 'TWRR': TWRRReturn(data),
        # 'GordonGrowth': GordonGrowthReturn(data),
        # 'FamaFrench': FamaFrenchReturn(data),
        # 'LinearRegression': LinearRegressionReturn(data),
        # 'RiskParity': RiskParityReturn(data),
        # 'BlackLitterman': BlackLittermanReturn(data),
        # # 'HoltWinters': HoltWintersReturn(data),
        # 'ARIMA': ARIMAReturn(data)
    }

    # Initialize an empty DataFrame to store returns
    df_returns = pd.DataFrame()

    # Loop through each return type and add to the DataFrame
    for return_type, calculator in return_calculators.items():
        return_values = calculator.calculate_expected_return()
        df_returns = update_returns_dataframe(df_returns, return_type, return_values)

    return df_returns


def get_expected_return(data):
    # Load stock data
    # data = get_stocks()
    # if data is empty, print error message and return
    if data.empty:
        print("Error: No stock data available.")
        return
        # Initialize an empty DataFrame to store returns
    df_returns = pd.DataFrame()

    # Run Monte Carlo Simulation
    max_sharpe_ratio, min_volatility = run_monte_carlo_simulation(data)

    # Update the DataFrame with max Sharpe ratio returns
    df_returns = update_returns_dataframe(df_returns, 'MaxSharpeRatio', max_sharpe_ratio[0])

    # Update the DataFrame with min volatility returns
    df_returns = update_returns_dataframe(df_returns, 'MinVolatility', min_volatility[0])

    # Calculate all other returns (Mean Historical, EMA Historical, CAPM)
    return calculate_all_returns(data)


if __name__ == "__main__":
    data = get_stocks()
    expected_return_df = get_expected_return(data)
    print(expected_return_df)
