""" This module contains the services for the API """

# pylint: disable=import-error
from ai import client


def create_new_assistant(name, instructions, tools, model):
    """ Creates a new assistant """
    assistant = client.beta.assistants.create(
        name=name,
        instructions=instructions,
        tools=tools,
        model=model,
    )
    return assistant


def create_new_thread():
    """ Creates a new thread """
    thread = client.beta.threads.create()
    return thread


def create_new_message(thread_id, role, content):
    """ Creates a new message """
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role=role,
        content=content,
    )
    return message


def create_new_run(thread_id, assistant_id, instructions):
    """ Creates a new run """
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions=instructions,
    )
    return run
