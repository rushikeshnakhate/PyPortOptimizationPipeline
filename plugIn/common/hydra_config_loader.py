import os
import logging
from abc import ABC, abstractmethod
import hydra
from omegaconf import DictConfig
from pathlib import Path

logger = logging.getLogger(__name__)


class HydraConfigLoader:
    def __init__(self):
        self._cfg = None
        self.config_loaded = False  # Track if the configuration is loaded

    def initialize_hydra(self, module_name: str):
        if not self.config_loaded:
            # Build the config directory relative to the current working directory
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
