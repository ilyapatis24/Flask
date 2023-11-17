from sqlalchemy import Column, DateTime, Integer, String, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
USER, PASS,DB_NAME, HOST, PORT = os.environ.get('POSTGRES_USER'), os.environ.get('POSTGRES_PASSWORD'),os.environ.get('POSTGRES_DB'),\
    os.environ.get('POSTGRES_HOST'), os.environ.get('POSTGRES_PORT')

engine = create_engine(f"postgresql://{USER}:{PASS}@{HOST}:{PORT}/{DB_NAME}")
Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)

class Advert(Base):            

    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=False)
    owner = Column(String, nullable=False)
    creation_date = Column(DateTime, server_default=func.now())

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)