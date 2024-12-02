import datetime
from typing import Any

import logfire
from gh_hooks_utils.payloads import InstallationEvent
from sqlmodel import Session, select

from knowmydevs.app_logger import logger
from knowmydevs.github.domain import Installation


async def handle(event: InstallationEvent, session: Session) -> None:
    logger.info(f"Handling Installation Event for {event.installation.id}")
    with logfire.span("Github Installation Event"):
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
    optional_values = {}

    if install_event.enterprise:
        optional_values["enterprise_id"] = install_event.enterprise.id
        optional_values["enterprise_name"] = install_event.enterprise.name

    if install_event.organization:
        optional_values["organization_id"] = install_event.organization.id
        optional_values["organization_login"] = install_event.organization.login

    return {
        **optional_values,
        "id": install_event.installation.id,
        "sender_id": install_event.sender.id,
        "sender_name": install_event.sender.name,
        "sender_login": install_event.sender.login,
        "installed_at": datetime.datetime.now(datetime.UTC),
    }
