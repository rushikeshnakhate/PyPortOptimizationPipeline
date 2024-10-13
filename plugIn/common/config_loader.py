import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ConfigLoader(ABC):
    @abstractmethod
    def load_config(self, module_name: str):
        """Abstract method to load configuration."""
        pass
