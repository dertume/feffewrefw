from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    api_id: int = Field(alias="API_ID")
    api_hash: str = Field(alias="API_HASH")
    session_string: str = Field(alias="SESSION_STRING")
    cmd_prefix: str = Field(default=".", alias="CMD_PREFIX")
    owner_id: int = Field(alias="OWNER_ID")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    enabled_modules: list[str] = [
        "abiense_userbot.modules.basic.help",
        "abiense_userbot.modules.basic.ping",
        "abiense_userbot.modules.basic.alive",
        "abiense_userbot.modules.basic.afk",
        "abiense_userbot.modules.basic.notes",
        "abiense_userbot.modules.basic.system",
    ]


settings = Settings()
