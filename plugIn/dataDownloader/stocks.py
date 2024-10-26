from base_asset import BaseAsset
from plugIn.common.execution_time_recorder import ExecutionTimeRecorder


class Stocks(BaseAsset):
    def __init__(self, start_date, end_date, data_source, tickers):
        super().__init__(start_date, end_date, data_source)
        self.tickers = tickers

    @ExecutionTimeRecorder(module_name=__name__)
    def fetch_data(self):
        return self.data_source.get_data(self.tickers, self.start_date, self.end_date)
