from typing import Literal

from pydantic import BaseModel, Field


class Settings(BaseModel):
    app_title: str = Field(alias="APP_TITLE")
    app_description: str = Field(alias="APP_DESCRIPTION")
    app_mode: Literal["dev", "prod"] = Field(alias="APP_MODE")
    app_host: str = Field(alias="APP_HOST")
    app_port: int = Field(alias="APP_PORT")
    app_allow_ips: str | list[str] = Field(alias="APP_ALLOW_IPS")
    app_sub_path: str = Field(default="", alias="APP_SUB_PATH")
    database_connection_url: str = Field(alias="DATABASE_CONNECTION_URL")

    @property
    def is_debug(self) -> bool:
        return self.app_mode == "dev"
