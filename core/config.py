from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel


class LogConfig(BaseModel):
    format: str = "%(name)s %(asctime)s %(levelname)s %(message)s"
    base_dir: str = "logs"
    backup_count: int = 5
    file_size: int = 5 * 1024 * 1024


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
        env_file=(".env.template", ".env")
    )
    logs: LogConfig = LogConfig()
    runwayml_api_key: str
    azure_endpoint: str
    dalle_api_key: str
    port: int = 8000
    host: str = "0.0.0.0"
    api_prefix: str = "/api"


settings = Settings()
