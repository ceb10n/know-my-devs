import datetime
from typing import Any

import logfire
from gh_hooks_utils.payloads import InstallationEvent
from gh_hooks_utils.payloads.install.installation_action_enum import (
    InstallationActionEnum,
)
from sqlmodel import Session, select

from knowmydevs.app_logger import logger
from knowmydevs.core.auth import cognito
from knowmydevs.core.utils import date_utils
from knowmydevs.github.domain import Installation
from knowmydevs.github.services import app_client_service


async def handle(event: InstallationEvent, session: Session) -> None:
    with logfire.span("Github Installation Event"):
        if not event.installation:
            logger.warning("Installation is not present in event")
            return None

        logger.info(
            f"Handling Installation Event for {event.installation.id}. Event sent by {event.sender.name}"
        )
        install_dict = adapt(event)

        installation = find_installation_by_id(
            id=event.installation.id, session=session
        )

        if installation:
            logger.debug(f"Updating Installation {event.installation.id}")
            for k, v in install_dict.items():
                setattr(installation, k, v)

            installation.updated_at = datetime.datetime.now(datetime.UTC)

        else:
            logger.debug(f"Creating Installation {event.installation.id}")
            installation = Installation(**install_dict)

        session.add(installation)
        session.flush()

        if event.action == InstallationActionEnum.CREATED:
            app_client = cognito.create_app_client(installation.id)

            if not app_client:
                logger.error(
                    f"Failed to create app client for installation {installation.id}"
                )
                return None

            app_client_service.create_app_client(
                installation.id,
                app_client.client_name,
                app_client.client_id,
                app_client.client_secret,
                session,
            )

        session.commit()

        logger.info(
            f"Installation Event of {installation.id} successfully handled"
        )


def find_installation_by_id(id: int, session: Session) -> Installation | None:
    with logfire.span("Find Installation By Id") as span:
        span.set_attribute("id", id)

        statement = select(Installation).where(Installation.id == id)
        results = session.exec(statement)

        return results.one_or_none()


def adapt(install_event: InstallationEvent) -> dict[str, Any]:
    optional_values: dict[str, Any] = {}

    if not install_event.installation:
        raise ValueError("Field installation is required")

    if install_event.enterprise:
        optional_values["enterprise_id"] = install_event.enterprise.id
        optional_values["enterprise_name"] = install_event.enterprise.name

    if install_event.organization:
        optional_values["organization_id"] = install_event.organization.id
        optional_values["organization_login"] = install_event.organization.login

    if install_event.installation.account:
        optional_values["account_id"] = install_event.installation.account.id
        optional_values["account_login"] = (
            install_event.installation.account.login
        )

    return {
        **optional_values,
        "id": install_event.installation.id,
        "app_id": install_event.installation.app_id,
        "app_slug": install_event.installation.app_slug,
        "target_type": install_event.installation.target_type,
        "sender_id": install_event.sender.id,
        "sender_name": install_event.sender.name,
        "sender_login": install_event.sender.login,
        "installed_at": datetime.datetime.now(datetime.UTC),
        "updated_at": date_utils.maybe_str_to_datetime(
            install_event.installation.updated_at
        ),
        "suspended_at": date_utils.maybe_str_to_datetime(
            install_event.installation.suspended_at
        ),
    }
