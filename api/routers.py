""" This module contains the application routes. """

# pylint: disable=import-error
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import get_db

from .assistant import assistant_id
from .services import (
    start_new_thread,
    get_thread,
    get_all_threads,
    send_message,
)

router = APIRouter()

# An endpoint to start a new chat session
@router.post("/chat")
def start_chat_session(db: Session = Depends(get_db)):
    """ Start a new chat session. """
    try:
        response = start_new_thread(db)
        return response
    except Exception as e:
        raise e


# An endpoint to get all chat sessions
@router.get("/chat")
def get_chat_sessions(db: Session = Depends(get_db)):
    """ Get all chat sessions. """
    try:
        response = get_all_threads(db)
        return response
    except Exception as e:
        raise e


# An endpoint to get a chat session
@router.get("/chat/{chat_id}")
def get_chat_session(chat_id: str, db: Session = Depends(get_db)):
    """ Get a chat session. """
    try:
        response = get_thread(db, chat_id)
        return response
    except Exception as e:
        raise e


# An endpoint to send a message
@router.post("/chat/{chat_id}")
def send_chat_message(chat_id: str, message: str, db: Session = Depends(get_db)):
    """ Send a message. """
    try:
        response = send_message(db, chat_id, message)
        return response
    except Exception as e:
        raise e

