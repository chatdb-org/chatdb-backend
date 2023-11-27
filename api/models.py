""" This module contains the database models. """

# pylint: disable=import-error
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .database import Base


class Chat(Base):
    """ This class represents the chat session table. """
    __tablename__ = 'chat'

    id = Column(String(255), primary_key=True)
    title = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)


class Message(Base):
    """ This class represents the message table. """
    __tablename__ = 'message'

    id = Column(String(255), primary_key=True, default=str(uuid4()))
    chat_id = Column(Integer, ForeignKey('chat.id'))
    sender = Column(String(255))
    content = Column(String(1000))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
