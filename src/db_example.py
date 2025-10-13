from sqlalchemy import create_engine, text

# connection string
data_base_url = "mysql+pymysql://root:secret@localhost:3306/pyhton-de"
# SQLAlchemy engine
engine = create_engine(data_base_url, echo=True, pool_size=5, max_overflow=10)

with engine.connect() as connection:
    with connection.begin():
        sql = text("INSERT into users (username,email) VALUES(:username, :email)")
        params = {"username": "valeria", "email": "valeria@example.com"}
        result = connection.execute(sql, params)
