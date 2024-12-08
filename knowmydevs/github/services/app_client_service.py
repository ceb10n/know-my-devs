import datetime

from sqlmodel import Session

from knowmydevs.core.config import app_config
from knowmydevs.github.domain import AppClient


def create_app_client(
    installation_id: int,
    client_secret: str,
    session: Session,
    commit: bool = False,
) -> AppClient:
    client = AppClient(
        id=installation_id,
        user_pool_id=app_config.aws_cognito_pool_id,
        partial_secret=client_secret[:5],
        created_at=datetime.datetime.now(datetime.UTC),
    )

    session.add(client)

    if commit:
        session.commit()

    return client
