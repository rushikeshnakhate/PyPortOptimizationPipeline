import logging
from pathlib import Path
from omegaconf import OmegaConf

from plugIn.common.config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class OmegaConfLoader(ConfigLoader):
    def load_config(self):
        """Load the configuration for the application using OmegaConf."""
        logger.info("Loading configuration using OmegaConf")
        config_path = Path(__file__).parent.parent / 'conf' / 'config.yaml'
        return OmegaConf.load(config_path)
