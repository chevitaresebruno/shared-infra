from typing import Any

from settings.settings import Settings


def load_settings_from_env() -> Settings:
    from os import environ

    keys: dict[str, Any] = {}

    for name, field in Settings.model_fields.items():
        field_name = field.alias or name
        env_var: str
        try:
            env_var = environ[field_name]
        except KeyError:
            raise ValueError(f"env var {field_name} not found")
        keys[field_name] = env_var

    return Settings(**keys)
