import logfire

from knowmydevs.core.config import app_config


def init_app() -> None:
    if app_config.in_observable_environment():
        logfire.configure(token=app_config.logfire_token.get_secret_value())
