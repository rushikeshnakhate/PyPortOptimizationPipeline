from abc import ABC, abstractmethod


class BaseRiskModel(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def calculate_risk_matrix(self):
        pass
