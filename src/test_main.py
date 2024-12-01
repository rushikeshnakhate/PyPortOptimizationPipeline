from pathlib import Path

from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.main import run_optimization_pipeline, project_directory

if __name__ == "__main__":
    tickers = ["HDFCBANK.NS", "RELIANCE.NS", "CIPLA.NS", "DIVISLAB.NS",
               "HDFCLIFE.NS", "BHARTIARTL.NS", "ASIANPAINT.NS", "INFY.NS"]
    run_optimization_pipeline(years=[2022, 2023, 2024], tickers=tickers)
    run_optimization_pipeline(years=[2022, 2023, 2024], tickers=tickers, frequency="multiyear")

    executionTimeRecorder_df = ExecutionTimeRecorder.get_performance_dataframe()
    executionTimeRecorder_df.to_pickle(Path(project_directory) / 'execution_time.pkl')
