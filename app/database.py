from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<databse_name>'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Amazing10880@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base = declarative_base()


# while True:
#     try:
#         conn = psycopg2.connect(host= 'localhost', database= 'fastapi', user='postgres', password='Amazing10880', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("database connection succesfull")
#         break
#     except Exception as error:
#         print("connection to db failed")
#         print(f"{error=}")
#         time.sleep(2)