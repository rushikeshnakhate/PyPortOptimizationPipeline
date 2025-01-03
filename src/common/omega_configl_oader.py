import logging
from pathlib import Path
from omegaconf import OmegaConf

from src.common.config_loader import BaseConfigLoader

logger = logging.getLogger(__name__)


class OmegaConfLoader(BaseConfigLoader):
    def load_config(self):
        """Load the configuration for the application using OmegaConf."""
        logger.info("Loading configuration using OmegaConf")
        config_path = Path(__file__).parent.parent / 'conf' / 'config.yaml'
        return OmegaConf.load(config_path)
