from sqlalchemy import create_engine, Column, Integer, String, Sequence, Float,PrimaryKeyConstraint, ForeignKey,Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql import *

Database_url = "mysql://resume:n3tBanking@resumes.cvuksgsuaytw.us-east-1.rds.amazonaws.com:3306/resumes"
engine = create_engine(Database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "User"
    id = Column(Integer,primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(Text)

User.__table__.create(bind=engine, checkfirst=True)

