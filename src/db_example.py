from datetime import datetime
from typing import Sequence, Type

from sqlalchemy import DateTime, String, create_engine, insert, select, update
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

# connection string
data_base_url = "mysql+pymysql://root:secret@localhost:3306/pyhton-de"
# SQLAlchemy engine
engine = create_engine(data_base_url, echo=True, pool_size=5, max_overflow=10)

# metadata = MetaData()

# users_table = Table(
#   "users",
#   metadata,
#   Column("id", Integer, primary_key=True),
#   Column("username", String(50), nullable=False, unique=True),
#   Column("email", String(100), nullable=False),
#   Column("created_at", DateTime, default=datetime.utcnow),
# )
# comments_table = Table(
#    "comments",
#   metadata,
#   Column("id", Integer, primary_key=True),
#   Column("user_id", String(50), nullable=False), #should be foreign key
#   Column("ecomment", String(255), nullable=False),
#   Column("created_at", DateTime, default=datetime.utcnow),
# )


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    # id=Column("id", Integer, primary_key=True)
    # username=Column("username", String(50), nullable=False, unique=True)
    # email=Column("email", String(100), nullable=False)
    # created_at=Column("created_at", DateTime, default=datetime.utcnow)

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Comment(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(String(50), nullable=False)
    ecomment: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

with Session() as session:
    query = select(User).where(User.username == "alice")
    result = session.execute(query)
    user = result.scalars().one()
    print(type(user), user)
    query2 = select(User)
    result2 = session.execute(query2)
    user2 = result2.scalars().all()
    for use_r in user2:
        print(use_r.username, use_r.email)
    # update column value in table (email)
    user.email = "alice-new@example.com"
    session.commit()


def retrieve_all_users_db(User: Type[User]) -> Sequence[User]:
    Session_ = sessionmaker(bind=engine)
    with Session_() as session:
        query = select(User)
        result = session.execute(query)
        user = result.scalars().all()
    return user


def retrieve_user_by_username(User: Type[User], usernamee: str) -> User:
    Session_ = sessionmaker(bind=engine)
    with Session_() as session:
        query = select(User).where(User.username == usernamee)
        result = session.execute(query)
        user = result.scalars().one()
    return user


def insert_user_into_db(User: Type[User], usernamee: str, email: str) -> None:
    Session_ = sessionmaker(bind=engine)
    with Session_() as session:
        stmt = insert(User).values(username=usernamee, email=email)
        session.execute(stmt)
        session.commit()
        print(f"New user inserted: username:'{usernamee}', email:'{email}'")


def update_user_info(User: Type[User], user_id: int, username: str, email: str) -> None:
    Session_ = sessionmaker(bind=engine)
    with Session_() as session:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(username=username, email=email)
        )
        session.execute(stmt)
        session.commit()
        print(
            f"User with ID {user_id} is updated with new info: "
            f"username: '{username}', email: '{email}'"
        )


print("=" * 50)
print("Performing the 2 queries and the 2 transactions:")
all_users = retrieve_all_users_db(User)
for userr in all_users:
    print(userr.username, userr.email)
valeria = retrieve_user_by_username(User, "valeria")
print(valeria.username, valeria.email)
insert_user_into_db(User, "Vakin", "Vakin@example.com")
update_user_info(User, 7, "Haaland", "Haaland@mancity.com")
