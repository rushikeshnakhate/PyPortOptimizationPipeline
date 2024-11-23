import pandas as pd


class MockARIMAReturn:
    def __init__(self, data):
        self.data = data

    def calculate_expected_return(self, output_dir):
        # Simulating a return values DataFrame
        return pd.DataFrame({
            'Ticker': ['AAPL', 'GOOGL'],
            'ExpectedReturn_ARIMA': [0.05, 0.04]
        }).set_index('Ticker')


class MockArithmeticMeanHistoricalReturn:
    def __init__(self, data):
        self.data = data

    def calculate_expected_return(self, output_dir):
        # Simulating a return values DataFrame
        return pd.DataFrame({
            'Ticker': ['AAPL', 'GOOGL'],
            'ExpectedReturn_ArithmeticMeanHistorical': [0.02, 0.03]
        }).set_index('Ticker')


class MockBlackLittermanReturn:
    def __init__(self, data):
        self.data = data

    def calculate_expected_return(self, output_dir):
        # Simulating a return values DataFrame
        return pd.DataFrame({
            'Ticker': ['AAPL', 'GOOGL'],
            'ExpectedReturn_BlackLitterman': [0.03, 0.02]
        }).set_index('Ticker')

# Add other mocks for other return calculators if necessary
