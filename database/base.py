# coding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#engine = create_engine('postgresql://postgres:postgres@172.17.0.3:5432/utenotificaciones')
engine = create_engine('oracle://ute:ute@172.17.0.2:1521/ORCLCDB')

Session = sessionmaker(bind=engine)

Base = declarative_base()