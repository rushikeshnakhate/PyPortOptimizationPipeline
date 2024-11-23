from pydantic.dataclasses import dataclass


@dataclass
class AssetTypeConventions:
    stocks: str = "stocks"
    bonds: str = "bonds"


@dataclass
class SourceTypeConventions:
    YahooFinance: str = "YahooFinance"
    AlphaVantage: str = "AlphaVantage"
    CustomCSV: str = "CustomCSV"
