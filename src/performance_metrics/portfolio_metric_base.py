from abc import abstractmethod, ABC


class PortfolioMetricBase(ABC):
    def __init__(self, config=None):
        self.config = config or {}

    @abstractmethod
    def calculate(self, portfolio, precalculated_metrics=None):
        """
        Calculate the metric for the given portfolio.

        Args:
            portfolio (Portfolio): The portfolio object for which to calculate the metric.

        Returns:
            float: The calculated metric value.
            :param portfolio:
            :param precalculated_metrics:
        """
        pass
