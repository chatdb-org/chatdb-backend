""" This module contains the database models. """

# pylint: disable=import-error
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .database import Base


class ChatSession(Base):
    """ This class represents the chat session table. """
    __tablename__ = 'chat_session'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Message(Base):
    """ This class represents the message table. """
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, index=True)
    chat_session_id = Column(Integer, ForeignKey('chat_session.id'))
    sender_id = Column(String(255))
    message = Column(String(1000))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
