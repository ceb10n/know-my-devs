import sentry_sdk

from knowmydevs.core.config import app_config


def init_app() -> None:
    if app_config.in_observable_environment():
        sentry_sdk.init(
            dsn=app_config.sentry_dns,
            traces_sample_rate=app_config.sentry_trace_rate,
            _experiments={
                "continuous_profiling_auto_start": True,
            },
        )