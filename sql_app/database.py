from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
#SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'
SQLALCHEMY_DATABASE_URL = "postgresql://tkksctwo:password@localhost/bigbbe"
#SQLALCHEMY_DATABASE_URL = "postgresql://umoadbahsoebsr:f9a8d588f48602074fd34936e954521b42d060053706284c166cf8a3031e3be5@ec2-44-194-92-192.compute-1.amazonaws.com:5432/d4mb36nr11omsp"

engine = create_engine(
    # SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()