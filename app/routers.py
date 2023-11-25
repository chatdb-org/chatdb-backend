""" This module contains the application routes. """

# pylint: disable=import-error
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import get_db
from .models import ChatSession, Message

router = APIRouter()


@router.get("/chat_session")
def get_chat_sessions(db: Session = Depends(get_db)):
    """Get all chat sessions."""
    return db.query(ChatSession).all()


@router.get("/chat_session/{chat_session_id}")
def get_chat_session(chat_session_id: int, db: Session = Depends(get_db)):
    """Get a chat session by id."""
    chat_session = (
        db.query(ChatSession).filter(ChatSession.id == chat_session_id).first()
    )
    if not chat_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    return chat_session


# send a message

