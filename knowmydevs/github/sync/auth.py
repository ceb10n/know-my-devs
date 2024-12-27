from gh_hooks_utils.auth import app_auth


def auth_with_installation(installation_id: int, client_id: int):
    return app_auth.authenticate(
        installation_id,
        clinent_id=client_id,
    )
