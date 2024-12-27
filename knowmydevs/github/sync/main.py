from knowmydevs.core.infra.db import postgres
from knowmydevs.github.domain import HistoricalData
from knowmydevs.github.services import historical_data_service
from knowmydevs.github.sync import auth


if __name__ == "__main__":
    postgres.init_app()
    session = postgres.get_session()

    page = 1
    limit = 10

    data = historical_data_service.list_all_that_need_to_sync(
        page, limit, session
    )

    while data:
        page += 1
        data = historical_data_service.list_all_that_need_to_sync(
            page, limit, session
        )

        for historical_data in data:
            token = auth.auth_with_installation(
                historical_data.installation_id, historical_data.client_id
            )
            print(token)
