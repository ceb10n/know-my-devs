import logfire
from sqlmodel import Session

from knowmydevs.github.domain import User


def add_user(user: User, session: Session) -> None:
    with logfire.span("Create user {id}", user.id):
        session.add(user)
        session.commit()


def find_by_id(id: int, session: Session) -> User | None:
    with logfire.span("Searh for user {id}", id=id):
        return session.get(User, id)
