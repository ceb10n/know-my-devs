from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, asc, delete, select

from knowmydevs.app_logger import logger
from knowmydevs.core.errors import BadRequestError, InternalError, NotFoundError
from knowmydevs.github.domain.pull_request import PullRequest
from knowmydevs.github.payloads.prs import (
    CreatePullRequestPayload,
    UpdatePullRequestPayload,
)
from knowmydevs.github.responses.prs import PullRequestResponse


def create_pull_request(
    pull_request: CreatePullRequestPayload,
    installation_id: int,
    session: Session,
) -> PullRequestResponse:
    logger.info(
        f"Creating pull request {pull_request.id} for installation {installation_id}"
    )
    new_pull_request = PullRequest(
        installation_id=installation_id, **pull_request.model_dump()
    )

    try:
        session.add(new_pull_request)
        session.commit()

    except IntegrityError as ex:
        logger.warning(f"Pull Request alreay exists: {ex}")
        session.rollback()

        raise BadRequestError("Pull Request already exists") from ex

    except Exception as ex:
        logger.error(f"Error creating pull request: {ex}")
        session.rollback()

        raise InternalError("Error creating pull request") from ex

    return PullRequestResponse(**pull_request.model_dump())


def delete_pull_request(
    pull_request_id: int,
    installation_id: int,
    session: Session,
) -> None:
    logger.info(
        f"Deleting pull request {pull_request_id} for installation {installation_id}"
    )
    statement = delete(PullRequest).where(
        PullRequest.id == pull_request_id
        and PullRequest.installation_id == installation_id
    )

    session.exec(statement)
    session.commit()


def find_pull_request_by_id(
    pull_request_id: int,
    installation_id: int,
    session: Session,
) -> PullRequestResponse:
    logger.info(
        f"Looking for Pull Request {pull_request_id} for installation {installation_id}"
    )
    statement = select(PullRequest).where(
        PullRequest.id == pull_request_id
        and PullRequest.installation_id == installation_id
    )
    existing_pull_request = session.exec(statement).one_or_none()

    if not existing_pull_request:
        raise NotFoundError(f"Pull Request with id {pull_request_id} not found")

    return PullRequestResponse(**existing_pull_request.model_dump())


def list_pull_requests(
    page: int,
    limit: int,
    installation_id: int,
    session: Session,
) -> list[PullRequestResponse]:
    logger.info(f"Listing pull requests for installation {installation_id}")

    statement = (
        select(PullRequest)
        .where(PullRequest.installation_id == installation_id)
        .order_by(asc(PullRequest.created_at))
        .limit(limit)
        .offset((page - 1) * limit)
    )

    prs = session.exec(statement).all()

    return [PullRequestResponse(**f.model_dump()) for f in prs]


def update_pull_request(
    pull_request_id: int,
    pull_request: UpdatePullRequestPayload,
    installation_id: int,
    session: Session,
) -> PullRequestResponse:
    logger.info(
        f"Updating pull request {pull_request_id} for installation {installation_id}"
    )

    statement = select(PullRequest).where(
        PullRequest.id == pull_request_id
        and PullRequest.installation_id == installation_id
    )
    existing_pull_request = session.exec(statement).one_or_none()

    if not existing_pull_request:
        raise NotFoundError(f"Pull Request with id {pull_request_id} not found")

    for key, value in pull_request.model_dump().items():
        try:
            setattr(existing_pull_request, key, value)

        except Exception as ex:
            err_msg = f"Invalid value {value} for property {key}"
            logger.debug(f"{err_msg}: {ex}")

            raise BadRequestError(err_msg) from ex

    try:
        response = PullRequestResponse(**existing_pull_request.model_dump())
        session.add(existing_pull_request)
        session.commit()

        return response

    except Exception as ex:
        err_msg = f"Error updating pull request with id {pull_request_id}"
        logger.error(f"{err_msg}: {ex}")
        session.rollback()

        raise InternalError(err_msg) from ex
