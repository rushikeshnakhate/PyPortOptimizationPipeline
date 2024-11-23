import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class BaseConfigLoader(ABC):
    @abstractmethod
    def load_config(self, module_name: str):
        """Abstract method to load configuration."""
        pass
