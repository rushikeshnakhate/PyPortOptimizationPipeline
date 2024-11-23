from base_asset import BaseAsset


class Commodities(BaseAsset):
    def __init__(self, start_date, end_date, data_source):
        super().__init__(start_date, end_date, data_source)

    def fetch_data(self, tickers):
        return self.data_source.get_data(tickers, self.start_date, self.end_date)
