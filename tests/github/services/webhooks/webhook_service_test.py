from unittest import mock

import pytest
from gh_hooks_utils import EventsEnum

from knowmydevs.github.services.webhooks import webhook_service

from ...data.discussion.data import dicussion_closed, discussion_answered
from ...data.discussion_comment.data import discussion_comment_created
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
            install_event_all_repos,
            b"",
            headers_mock(EventsEnum.INSTALLATION),
            None,
        )

    except Exception as ex:
        pytest.fail(
            f"test_handle_webhook_for_installation_created failed: {ex}"
        )


@mock.patch(TARGET_CALL_HANDLER, mock_call_handler)
@mock.patch(TARGET_CONFIG, config_mock())
@pytest.mark.asyncio
async def test_handle_webhook_for_discussion_comment_created():
    try:
        await webhook_service.handle_webhook(
            discussion_comment_created,
            b"",
            headers_mock(EventsEnum.DISCUSSION_COMMENT),
            None,
        )

    except Exception as ex:
        pytest.fail(f"test_handle_webhook_for_discussion_created failed: {ex}")


@mock.patch(TARGET_CALL_HANDLER, mock_call_handler)
@mock.patch(TARGET_CONFIG, config_mock())
@pytest.mark.asyncio
async def test_handle_webhook_for_discussion_answered():
    try:
        await webhook_service.handle_webhook(
            discussion_answered, b"", headers_mock(EventsEnum.DISCUSSION), None
        )

    except Exception as ex:
        pytest.fail(f"test_handle_webhook_for_discussion_answered failed: {ex}")


@mock.patch(TARGET_CALL_HANDLER, mock_call_handler)
@mock.patch(TARGET_CONFIG, config_mock())
@pytest.mark.asyncio
async def test_handle_webhook_for_discussion_closed():
    try:
        await webhook_service.handle_webhook(
            dicussion_closed, b"", headers_mock(EventsEnum.DISCUSSION), None
        )

    except Exception as ex:
        pytest.fail(f"test_handle_webhook_for_discussion_closed failed: {ex}")
