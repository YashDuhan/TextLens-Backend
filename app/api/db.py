import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends, HTTPException

# Load env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise HTTPException(status_code=500, detail="DATABASE_URL is not set.")

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define base for model classes
Base = declarative_base()

# model schema
class PDFMetadata(Base):
    __tablename__ = "main_pdf_metadata"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    filesize = Column(Integer, nullable=False)
    filecontent = Column(String, nullable=False)
    uploaddate = Column(DateTime, nullable=False)
    s3_url = Column(String, nullable=False)

# get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize tables in the database
Base.metadata.create_all(bind=engine)
