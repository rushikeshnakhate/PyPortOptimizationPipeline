import pandas as pd

from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.dataDownloader.base_data_downloader import BaseDataDownloader
import logging

logger = logging.getLogger(__name__)


class BondDataDownloader(BaseDataDownloader):
    def __init__(self, start_date, end_date, current_dir):
        super().__init__('bonds', start_date, end_date, current_dir)

    @ExecutionTimeRecorder(module_name='download_bonds')
    def download_data(self):
        # Implement bond data download logic here
        logger.info(f"Fetching bond data for {self.start_date} to {self.end_date}")
        # For demo purposes, return an empty DataFrame
        return pd.DataFrame()