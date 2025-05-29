from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from models.contacts import Base

class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    is_sent = Column(Boolean, nullable=False)  # True = sent, False = received
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=False)

    contact = relationship('Contact', backref='messages')

    def __repr__(self):
        direction = "Sent" if self.is_sent else "Received"
        return f"{direction}: {self.content}"

