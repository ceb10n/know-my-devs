from unittest import mock

import pytest

from knowmydevs.github.services.webhooks import webhook_service

from ...data.installation.data import install_event_all_repos
from .mocks import config_mock, headers_mock
from .webhook_service_mock import (
    TARGET_CALL_HANDLER,
    TARGET_CONFIG,
    mock_call_handler,
)


@mock.patch(TARGET_CALL_HANDLER, mock_call_handler)
@mock.patch(TARGET_CONFIG, config_mock())
@pytest.mark.asyncio
async def test_handle_webhook_for_installation_created():
    try:
        await webhook_service.handle_webhook(
            install_event_all_repos, b"", headers_mock(), None
        )

    except Exception as ex:
        pytest.fail(
            f"test_handle_webhook_for_installation_created failed: {ex}"
        )