from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel

from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas, utils
from .database import engine, get_db
from .utils import pwd_context
from sqlalchemy.orm import Session
from .routers import post, users, auth
from pydantic_settings import BaseSettings
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Settings(BaseSettings):
    database_password: str
    database_username: str = "postgres"
    secret_key: str = "2345eff55323657"

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

# my_posts = [{"title": "title of post1", "content": "content of post1", "id":1},{"title": "favourite food", "content": "i like pizza", "id":2}]

@app.get('/')
def root():
    return {"message": "hello world!!!!"}

@app.get('/sqlalchemy')
def test_posts(db:Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # print(posts)
    return {"data": posts}


    
    
# @app.post('/posts')
# def create_posts(payLoad: dict= Body(...)):
#     print(payLoad)
#     return {"message": "post created"}


app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)