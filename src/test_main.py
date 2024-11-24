from pathlib import Path

from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.main import run_optimization_pipeline, project_directory

if __name__ == "__main__":
    run_optimization_pipeline(years=[2020], months=[1, 4], frequency="monthly")
    executionTimeRecorder_df = ExecutionTimeRecorder.get_performance_dataframe()
    executionTimeRecorder_df.to_pickle(Path(project_directory) / 'execution_time.pkl')
