""" This module creates the assistant. """

# pylint: disable=import-error
import os
from openai import OpenAI
from .config import openai_api_key, assistant_id


if not openai_api_key:
    print("OpenAI API key not found. Please set it in config.py")
    exit(1)

client = OpenAI(api_key=openai_api_key)
if not assistant_id:
    files = []
    for f in os.listdir('data'):
        file = client.files.create(
            file=open('data/' + f, 'rb'),
            purpose='assistants',
        )
        files.append(file.id)


    assistant = client.beta.assistants.create(
        name="ChatDB",
        description="A chatbot that simolifies data for businesses by enabling non-tech users to effortlessly query e-commerce databases using everyday language, bridging the gap between complex data management and intuitive user experience.",
        instructions="Hey ChatDB, your mission is to enhance user experience and facilitate effortless interactions. When engaging with users querying the e-commerce database, prioritize simplicity and clarity. Respond promptly, using straightforward language that resonates with non-tech users. Guide them through the process patiently, ensuring a seamless and intuitive experience. Foster a positive atmosphere, embodying a helpful and approachable persona. Remember, the goal is to bridge the gap between complex data and user-friendly engagement. Empower users to effortlessly navigate and extract valuable insights. Keep it simple, keep it user-centric, and always aim to make data interaction an enjoyable journey.",
        model="gpt-4-1106-preview",
        tools=[{"type": "code_interpreter"}, {"type": "retrieval"}],
        file_ids=files,
    )
    if assistant.id:
        print("Assistant created successfully.")
        print("Assistant id: " + assistant.id)

        with open('.env', 'a') as f:
            f.write('ASSISTANT_ID=' + assistant.id + '\n')
    else:
        print("Error creating assistant.")
        exit(1)
else:
    print("Assistant already created.")
    print("Assistant id: " + assistant_id)

