# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

PG_CONNECTION = os.getenv("PG_CONNECTION")
ORA_CONNECTION = os.getenv("ORA_CONNECTION")

if PG_CONNECTION:
    engine = create_engine(f'postgresql://{PG_CONNECTION}')
if ORA_CONNECTION:
    engine = create_engine(f'oracle://{ORA_CONNECTION}',pool_size=10, max_overflow=20,max_identifier_length=128)

if PG_CONNECTION or ORA_CONNECTION:
    SessionDB = sessionmaker(bind=engine)

    Base = declarative_base()

    # generate database schema
    result = Base.metadata.create_all(engine)