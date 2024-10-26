from base_asset import BaseAsset


class Bonds(BaseAsset):
    def __init__(self, start_date, end_date, data_source):
        super().__init__(start_date, end_date, data_source)

    def fetch_data(self):
        return self.data_source.get_data(self.tickers, self.start_date, self.end_date)
