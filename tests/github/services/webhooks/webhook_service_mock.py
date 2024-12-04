_base_module = "knowmydevs.github.services.webhooks.webhook_service"

TARGET_CALL_HANDLER = f"{_base_module}._call_handler_for_event"

TARGET_CONFIG = f"{_base_module}.app_config"


async def mock_call_handler(*_) -> None:
    pass
