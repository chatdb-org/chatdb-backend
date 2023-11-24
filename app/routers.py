""" This module contains the application routes. """

# pylint: disable=import-error
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import get_db
from .models import ChatSession, Message

router = APIRouter()


@router.get("/chat_session", response_model=List[ChatSession])
def get_chat_sessions(db: Session = Depends(get_db)):
    """Get all chat sessions."""
    return db.query(ChatSession).all()


@router.get("/chat_session/{chat_session_id}", response_model=ChatSession)
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


@router.post("/chat_session/{chat_session_id}/message", response_model=Message)
def send_message(
    chat_session_id: int,
    message: Message,
    db: Session = Depends(get_db)
):
    """Send a message to a chat session."""
    chat_session = (
        db.query(ChatSession).filter(ChatSession.id == chat_session_id).first()
    )
    if not chat_session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat session not found"
        )
    db_message = Message(
        chat_session_id=chat_session_id,
        sender_id=message.sender_id,
        message=message.message,
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
