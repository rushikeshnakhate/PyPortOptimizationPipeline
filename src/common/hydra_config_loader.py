import logging
import os

import hydra
from hydra.core.global_hydra import GlobalHydra
from omegaconf import DictConfig

from src.common.config_loader import BaseConfigLoader

logger = logging.getLogger(__name__)


class HydraConfigLoader(BaseConfigLoader):
    def __init__(self):
        self._cfg = None
        self.config_loaded = False  # Track if the configuration is loaded

    def initialize_hydra(self, module_name: str):
        if GlobalHydra.instance().is_initialized():
            GlobalHydra.instance().clear()

        if not self.config_loaded:
            # Build the config directory relative to the current working directory
            if module_name == "src":
                config_dir = os.path.join('../..', module_name)
            else:
                config_dir = os.path.join('..', module_name)
            # Initialize Hydra with the relative path
            hydra.initialize(config_path=config_dir, job_name="default", caller_stack_depth=1, version_base=None)
            self.config_loaded = True  # Mark as loaded

    def load_config(self, module_name: str, config_name: str = 'config') -> DictConfig:
        self.initialize_hydra(module_name)  # Ensure Hydra is initialized
        if self._cfg is None:
            self._cfg = hydra.compose(config_name=config_name)
        return self._cfg

    def get_config(self, module_name: str, config_name: str = 'config') -> DictConfig:
        return self.load_config(module_name, config_name)


def load_config(module_name):
    """Load the configuration for the returns module from its own config.yaml."""
    config_loader = HydraConfigLoader()
    returns_cfg = config_loader.get_config(module_name)
    logger.info(f"Loading configuration for the returns module_name={module_name} from config.yaml")
    return returns_cfg
