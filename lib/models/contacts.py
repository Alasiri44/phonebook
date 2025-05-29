from sqlalchemy import Column, Integer, String, Boolean
from  sqlalchemy.orm import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'
    
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=True)
    is_favorite = Column(Boolean, default=False)

    def __repr__(self):
        return f"Contact(name={self.name}, phone={self.phone}, email={self.email})"