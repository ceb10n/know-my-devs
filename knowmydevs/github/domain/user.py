from sqlmodel import BigInteger, Field, SQLModel


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(primary_key=True, sa_type=BigInteger)
    login: str = Field(index=True, unique=True, max_length=100)
    name: str | None = Field(max_length=150)
    email: str | None = Field(max_length=150)
    avatar_url: str = Field(max_length=200)
