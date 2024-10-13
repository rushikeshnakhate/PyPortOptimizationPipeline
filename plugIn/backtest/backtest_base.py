import logging
import pandas as pd

logger = logging.getLogger(__name__)


class BackTestBase:
    def __init__(self, data, output_dir):
        """
        Initialize the BackTest base class with financial data and output directory.

        Args:
            data (pd.DataFrame): The input data (e.g., stocks, derivatives, commodities).
            output_dir (Path): The directory where results will be saved.
        """
        self.data = data
        self.output_dir = output_dir
        self.df_returns = pd.DataFrame()

    def update_returns_dataframe(self, return_type, return_values):
        """
        Update the returns dataframe with new return values.

        Args:
            return_type (str): The type of return being calculated (e.g., 'CAGR', 'CAPM').
            return_values (list or pd.Series): The return values calculated for each asset.
        """
        return_series = pd.Series(return_values, name=return_type)
        logger.info(f"Updating returns dataframe with return type: {return_type}")
        self.df_returns = self.df_returns.join(return_series, how='outer')

    def save_results(self, filename='expected_returns.pkl'):
        """
        Save the dataframe of returns to a pickle file.

        Args:
            filename (str): The filename to save the results. Default is 'expected_returns.pkl'.
        """
        output_path = self.output_dir / filename
        logger.info(f"Saving returns dataframe to {output_path}")
        self.df_returns.to_pickle(output_path)

    def save_metrics(self, metrics, filename='evaluation_metrics.csv'):
        """
        Save evaluation metrics to a CSV file.

        Args:
            metrics (dict): A dictionary of metrics to be saved.
            filename (str): The filename to save the metrics. Default is 'evaluation_metrics.csv'.
        """
        metrics_df = pd.DataFrame(metrics).T
        output_path = self.output_dir / filename
        logger.info(f"Saving evaluation metrics to {output_path}")
        metrics_df.to_csv(output_path)

    def log_summary(self):
        """
        Log a summary of the results (e.g., shape of returns dataframe).
        """
        logger.info(f"Returns dataframe shape: {self.df_returns.shape}")
        logger.info(f"First few rows of returns dataframe: \n{self.df_returns.head()}")
