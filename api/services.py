""" This module contains all the services (functions). """
import json
import time
from openai import OpenAI
from sqlalchemy.orm import Session
from .assistant import client, assistant_id
from .responses import CustomResponse, CustomException
from .models import Chat, Message

from datetime import datetime
from typing import Any, Dict, List

from sqlalchemy.ext.declarative import DeclarativeMeta


def model_to_dict(models: List[DeclarativeMeta]) -> List[Dict[str, Any]]:
    """Converts a list of SQLAlchemy models to a list of dictionaries.

    Args:
        models (List[DeclarativeMeta]): List of SQLAlchemy models

    Returns:
        List[Dict[str, Any]]: A dictionary representations of the models
    """

    def convert_datetime(value: Any) -> Any:
        """Converts datetime objects to ISO format."""
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    result_list: List[Dict[str, Any]] = [
        {
            column.name: convert_datetime(getattr(model, column.name))
            for column in model.__table__.columns
        }
        for model in models
    ]

    return result_list

def wait_on_run(run, thread_id):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        print(run.status)
        time.sleep(1)
    return run

def generate_title(message):
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are ChatDB, a chatbot that helps non-technical people communicate with database, You are To generate a Title for this converstation"},
        {"role": "assistant", "content": "Hello, I am ChatDB, How can I help you today?"},
        {"role": "user", "content": message}
      ]
    )
    title = response.choices[0].message.content
    return title


def start_new_thread(db: Session):
    """ Start a new chat session. """
    try:
        thread = client.beta.threads.create()
        response = send_message(db, thread.id, "assistant", "Hello ChatDB, Start a Conversation")
        return response
        
    except Exception as e:
        print(e)
        db.rollback()
        raise e

    return message


def get_all_threads(db: Session):
    """ Get all chat sessions. """
    db_threads = db.query(Chat).all()
    # Sort messages by updated_at
    db_threads.sort(key=lambda x: x.updated_at, reverse=True)
    db_threads = model_to_dict(db_threads)

    return CustomResponse(
        status_code=200,
        message="success",
        data={
            "threads": db_threads,
        }
    )


def get_thread(db: Session, chat_id: str):
    """ Get a chat session. """
    db_thread = db.query(Message).filter(Message.chat_id == chat_id).all()
    # Sort messages by created_at
    db_thread.sort(key=lambda x: x.created_at)
    db_thread = model_to_dict(db_thread)
    return CustomResponse(
        status_code=200,
        message="success",
        data={
            "thread": db_thread,
        }
    )


def send_message(db: Session, chat_id: str, sender: str, message: str):
    """ Send a message. """
    message = client.beta.threads.messages.create(
        thread_id=chat_id,
        role="user",
        content=message
    )

    run = client.beta.threads.runs.create(
        thread_id=chat_id,
        assistant_id=assistant_id,
        instructions="Please carefully respond to the user and provide them a very satisfactory response"
    )
    run = wait_on_run(run, chat_id)

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=chat_id,
        )
        message = messages.data[0].content[0].text.value

        db_chat= db.query(Chat).filter(Chat.id == chat_id).first()
        if not db_chat:
            db_chat = Chat(
                    id=chat_id,
                    title="New Chat",
                )
            db.add(db_chat)
        else:
            if db_chat.title == "New Chat":
                db_chat.title = generate_title(message)
                db.add(db_chat)

        db_message = Message(
                id=messages.data[0].id,
                chat_id=chat_id,
                sender=sender,
                content=message
            )
        db.add(db_message)
        db.commit()
        db.refresh(db_chat)
        return CustomResponse(
            status_code=200,
            message="success",
            data={
                "chat_id": chat_id,
                "message_id": db_message.id,
                'title': db_chat.title,
                "message": message,
            }

        )
    else:
        return CustomException(
            status_code=500,
            message="failed",
            data={
                "chat_id": "",
            }
        )

