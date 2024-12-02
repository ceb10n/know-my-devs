import logging
import uuid

from gh_hooks_utils import EventsEnum
from gh_hooks_utils.headers import WebhookHeaders

from knowmydevs.core.config import AppConfig


def config_mock() -> AppConfig:
    return AppConfig(
        app_name="app",
        environment="test",
        gh_token="1234",
        logfire_token="4321",
        log_level=logging.DEBUG,
        pg_database="knowmydevs",
        pg_host="localhost",
        pg_port=1234,
        pg_username="username",
        pg_password="password",
        sentry_dns="https://sentry.io",
        sentry_trace_rate=1.0,
    )


def headers_mock() -> WebhookHeaders:
    return WebhookHeaders(
        x_github_event=EventsEnum.INSTALLATION.value,
        x_github_hook_id=str(uuid.uuid4()),
        x_github_delivery=str(uuid.uuid4()),
        user_agent="GitHub-Hookshot/testing",
        x_github_hook_installation_target_type="test",
        x_github_hook_installation_target_id=str(uuid.uuid4()),
    )
