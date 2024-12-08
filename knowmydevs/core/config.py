import logging

from pydantic import HttpUrl, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    app_name: str
    aws_region: str
    aws_cognito_pool_id: str
    environment: str = "local"
    gh_token: SecretStr
    logfire_token: SecretStr
    log_level: int = logging.INFO
    pg_database: str
    pg_host: str
    pg_port: int
    pg_username: str
    pg_password: SecretStr
    sentry_dns: HttpUrl
    sentry_trace_rate: float

    def is_test_environment(self) -> bool:
        return self.environment == "test"

    def is_local_environment(self) -> bool:
        return self.environment == "local"

    def in_observable_environment(self) -> bool:
        return True
        # return self.environment not in ("local", "test")


app_config = AppConfig()
