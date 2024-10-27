from plugIn.expected_return.expected_returns_base import ExpectedReturnBase
import yfinance as yf


class GordonGrowthReturn(ExpectedReturnBase):
    def __init__(self, data):
        super().__init__(data)
        self.tickers = data.columns
        self.data = {}
        self.fetch_data()

    # Fetch data from Yahoo Finance
    def fetch_data(self):
        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            info = stock.info
            dividend_yield = self.get_dividend_yield(info)
            growth_rate = self.get_growth_rate(info)
            self.data[ticker] = {
                'dividend_yield': dividend_yield,
                'growth_rate': growth_rate
            }

    # Helper method to get dividend yield
    def get_dividend_yield(self, info):
        dividend_yield = info.get('dividendYield', None)
        return dividend_yield if dividend_yield is not None else 0

    # Helper method to get growth rate
    def get_growth_rate(self, info):
        # Proxy for growth rate using earnings or revenue estimates
        earnings_growth = info.get('earningsQuarterlyGrowth', None)  # Quarterly earnings growth rate

        if earnings_growth is not None:
            return earnings_growth
        return 0

    # Calculate expected return for all tickers
    def _calculate_expected_return(self):
        expected_returns = {}
        for ticker, metrics in self.data.items():
            dividend_yield = metrics.get('dividend_yield', 0)
            growth_rate = metrics.get('growth_rate', 0)
            expected_returns[ticker] = dividend_yield + growth_rate
        return self._convert_to_dataframe(expected_returns)

    # Optionally, calculate expected return for a specific ticker
    def calculate_expected_return_for_ticker(self, ticker):
        metrics = self.data.get(ticker, {})
        dividend_yield = metrics.get('dividend_yield', 0)
        growth_rate = metrics.get('growth_rate', 0)
        return dividend_yield + growth_rate

    # Get all data
    def get_all_data(self):
        return self.data
