from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import time
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth
load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password=os.environ.get('DB_PASSWORD'), cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to database")
        break
    except Exception as e:
        time.sleep(3)
        print("Error connecting to database", e)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI"}
