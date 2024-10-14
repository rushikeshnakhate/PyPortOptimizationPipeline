import logging
from pathlib import Path

from plugIn.backtest.backtest_base import BackTestBase
from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.expected_return.arithmetic_mean_historical_return import ArithmeticMeanHistoricalReturn
from plugIn.expected_return.black_litterman import BlackLittermanReturn
from plugIn.expected_return.cagr_mean_historical_return import CAGRMeanHistoricalReturn
from plugIn.expected_return.capm_return import CAPMReturn
from plugIn.expected_return.ema_historical_return import EMAHistoricalReturn
from plugIn.expected_return.fama_french import FamaFrenchReturn
from plugIn.expected_return.gordon_growth import GordonGrowthReturn
from plugIn.expected_return.machine_learning_linearRegression import LinearRegressionReturn
from plugIn.expected_return.risk_parity import RiskParityReturn

logger = logging.getLogger(__name__)


class BackTestExpectedReturn(BackTestBase):
    def __init__(self, data, output_dir):
        """
        Initialize the BackTestExpectedReturn class with financial data and output directory.

        Args:
            data (pd.DataFrame): The input data for expected return calculations.
            output_dir (Path): The directory where results will be saved.
        """
        super().__init__(data, output_dir)

    @ExecutionTimeRecorder(module_name=__name__)  # Use __name__ t
    def calculate_expected_returns(self):
        """
        Calculate expected returns using various methods and update the returns dataframe.
        """
        logger.info("Calculating expected returns using various methods...")

        # Create a mapping of return types to their respective classes
        return_calculators = {
            'CAGRMeanHistorical': CAGRMeanHistoricalReturn(self.data),
            'ArithmeticMeanHistorical': ArithmeticMeanHistoricalReturn(self.data),
            'EMAHistorical': EMAHistoricalReturn(self.data),
            'CAPM': CAPMReturn(self.data),
            'GordonGrowth': GordonGrowthReturn(self.data),
            'FamaFrench': FamaFrenchReturn(self.data),
            'LinearRegression': LinearRegressionReturn(self.data),
            'RiskParity': RiskParityReturn(self.data),
            'BlackLitterman': BlackLittermanReturn(self.data),
        }

        # Loop through each return type and add to the DataFrame
        for return_type, calculator in return_calculators.items():
            return_values = calculator.calculate_expected_return()
            self.update_returns_dataframe(return_type, return_values)

        # Save the results to a file
        self.save_results()

    def evaluate_metrics(self):
        """
        Evaluate and save metrics for the expected returns.
        """
        metrics = {
            'Mean Return': self.df_returns.mean(),
            'Standard Deviation': self.df_returns.std(),
            'Sharpe Ratio': self.df_returns.mean() / self.df_returns.std(),
            # Add more metrics as needed
        }

        self.save_metrics(metrics)

    def run(self):
        """
        Run the backtest for expected returns.
        """
        self.calculate_expected_returns()
        self.evaluate_metrics()
        self.log_summary()

