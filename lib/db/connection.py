from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///phonebook.db', echo = False)
Session = sessionmaker(bind=engine)
session = Session()