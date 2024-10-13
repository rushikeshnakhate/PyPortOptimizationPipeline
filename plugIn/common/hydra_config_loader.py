import os
import logging
from abc import ABC, abstractmethod
import hydra
from omegaconf import DictConfig
from pathlib import Path

from plugIn.common.config_loader import ConfigLoader

logger = logging.getLogger(__name__)


class HydraConfigLoader(ConfigLoader):
    def __init__(self):
        self._cfg = None

    def load_config(self, module_name: str) -> DictConfig:
        # Build the config directory relative to the current working directory
        # Note: We're ensuring that we point directly to the intended module's directory.
        config_dir = os.path.join('..', module_name)  # This should be the relative path

        # Initialize Hydra with the relative path
        hydra.initialize(config_path=config_dir, job_name="default", caller_stack_depth=1,
                         version_base=None)  # Ensure the path is a string
        self._cfg = hydra.compose(config_name='config')  # Adjust this if your config file has a different name
        return self._cfg

    def get_config(self, module_name: str) -> DictConfig:
        return self.load_config(module_name)
