""" This module contains all the services (functions). """
import json
import time
from openai import OpenAI
from sqlalchemy.orm import Session
from .assistant import client, assistant_id


def parse_json(obj):
    json_str = obj.model_dump_json()
    parsed_json = json.loads(json_str)
    return parsed_json

def wait_on_run(run, thread_id):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        print(run.status)
        time.sleep(1)
    return run

def start_new_thread(db: Session):
    """ Start a new chat session. """
    thread = client.beta.threads.create()
    return {"thread_id": parse_json(thread)}

def get_all_threads(db: Session):
    """ Get all chat sessions. """
    return {"chat_id": "123"}

def get_thread(db: Session, chat_id: str):
    """ Get a chat session. """
    return {"chat_id": "123"}

def send_message(db: Session, chat_id: str, message: str):
    """ Send a message. """
    message = client.beta.threads.messages.create(
        thread_id=chat_id,
        role="user",
        content=message
    )

    run = client.beta.threads.runs.create(
        thread_id=chat_id,
        assistant_id=assistant_id,
        instructions="Please carefully respond to the user and provide them a very satisfactory response. The user has a premium account."
    )

    run = wait_on_run(run, chat_id)

    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=chat_id,
        )
        return {"messages": parse_json(messages)}
    else:
        return {"messages": "error"}

