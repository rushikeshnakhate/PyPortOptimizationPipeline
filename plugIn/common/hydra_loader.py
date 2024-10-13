import logging
import hydra
from omegaconf import DictConfig

logger = logging.getLogger(__name__)


class HydraConfigLoader(ConfigLoader):
    @hydra.main(config_path='conf', config_name='config')
    def load_config(self) -> DictConfig:
        """Load the configuration for the application using Hydra."""
        logger.info("Loading configuration using Hydra")
        return self._cfg  # Assuming this is set in the decorated method

    # Method to call load_config
    def get_config(self):
        return self.load_config()
