from abc import ABC, abstractmethod


class BaseAsset(ABC):
    def __init__(self, start_date, end_date, data_source):
        self.start_date = start_date
        self.end_date = end_date
        self.data_source = data_source

    @abstractmethod
    def fetch_data(self):
        """Fetch data from the data source."""
        pass
