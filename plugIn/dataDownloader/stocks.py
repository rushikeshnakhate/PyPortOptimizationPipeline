from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.dataDownloader.base_asset import BaseAsset


class Stocks(BaseAsset):
    def __init__(self, start_date, end_date, data_source):
        super().__init__(start_date, end_date, data_source)

    @ExecutionTimeRecorder(module_name=__name__)
    def fetch_data(self, tickers):
        return self.data_source.get_data(tickers, self.start_date, self.end_date)
