from sqlalchemy import Column, Integer, String
from  sqlalchemy.orm import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'
    
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)

    def __repr__(self):
        return f"Contact(name={self.name}, phone={self.phone}, email={self.email})"