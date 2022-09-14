from pathlib import Path

import yaml
from pydantic import ValidationError

from glvars.schemas import GlVarsConfig


class Loader:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> GlVarsConfig:
        try:
            data = self.read()
        except Exception:
            raise ReadConfigError("Failed to read config file.")
        try:
            return GlVarsConfig(**data)
        except ValidationError as e:
            raise ConfigSchemaError(f"Schema does not meet the requirements.\n{e}")

    def read(self) -> dict:
        with open(self.path, "r") as stream:
            data = yaml.load(stream, Loader=yaml.CLoader)
        return data


class LoaderError(Exception):
    """Base loader exception."""


class ReadConfigError(LoaderError):
    """Failed to read config file."""


class ConfigSchemaError(LoaderError):
    """Bad config schema."""
