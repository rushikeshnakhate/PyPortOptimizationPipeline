from pydantic.dataclasses import dataclass


@dataclass
class PerformanceMetricsNameConventions:
    portfolio_return: str = "PortfolioReturn"
    portfolio_volatility: str = "PortfolioVolatility"
