from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.contacts import Base

class Call(Base):
    __tablename__ = 'calls'

    id = Column(Integer, primary_key=True)
    call_type = Column(String, nullable=False)  # "incoming", "outgoing", "missed"
    timestamp = Column(DateTime, default=datetime.now())
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=False)

    contact = relationship('Contact', backref='calls')

    def __repr__(self):
        return f"{self.call_type.capitalize()} call with {self.contact.name} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
