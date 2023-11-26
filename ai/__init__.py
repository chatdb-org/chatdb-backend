""" This file is used to initialize the AI module """

# pylint: disable=import-error
from openai import OpenAI

client = OpenAI()
assistant = client.beta.assistants.create(
    name="Database Assistant",
    instructions="""
    	You are to retrieve relevant information from the Database using natural language queries. Enable users to effortlessly interact with the database by asking questions like 'What are the top-selling items?' or 'Show me product reviews with 4 stars or above.' Make the system user-friendly for non-tech folks, bridging the gap between complex data and a smooth, intuitive experience. Here is the database data:
		+--------------+------------------------+------------+-------------+-----------------------+------------------------+
		| TABLE_NAME   | COLUMN_NAME            | DATA_TYPE  | IS_NULLABLE | REFERENCED_TABLE_NAME | REFERENCED_COLUMN_NAME |
		+--------------+------------------------+------------+-------------+-----------------------+------------------------+
		| customers    | addressLine1           | varchar    | NO          | NULL                  | NULL                   |
		| customers    | addressLine2           | varchar    | YES         | NULL                  | NULL                   |
		| customers    | city                   | varchar    | NO          | NULL                  | NULL                   |
		| customers    | contactFirstName       | varchar    | NO          | NULL                  | NULL                   |
		| customers    | contactLastName        | varchar    | NO          | NULL                  | NULL                   |
		| customers    | country                | varchar    | NO          | NULL                  | NULL                   |
		| customers    | creditLimit            | decimal    | YES         | NULL                  | NULL                   |
		| customers    | customerName           | varchar    | NO          | NULL                  | NULL                   |
		| customers    | customerNumber         | int        | NO          | NULL                  | NULL                   |
		| customers    | phone                  | varchar    | NO          | NULL                  | NULL                   |
		| customers    | postalCode             | varchar    | YES         | NULL                  | NULL                   |
		| customers    | salesRepEmployeeNumber | int        | YES         | employees             | employeeNumber         |
		| customers    | state                  | varchar    | YES         | NULL                  | NULL                   |
		| employees    | email                  | varchar    | NO          | NULL                  | NULL                   |
		| employees    | employeeNumber         | int        | NO          | NULL                  | NULL                   |
		| employees    | extension              | varchar    | NO          | NULL                  | NULL                   |
		| employees    | firstName              | varchar    | NO          | NULL                  | NULL                   |
		| employees    | jobTitle               | varchar    | NO          | NULL                  | NULL                   |
		| employees    | lastName               | varchar    | NO          | NULL                  | NULL                   |
		| employees    | officeCode             | varchar    | NO          | offices               | officeCode             |
		| employees    | reportsTo              | int        | YES         | employees             | employeeNumber         |
		| offices      | addressLine1           | varchar    | NO          | NULL                  | NULL                   |
		| offices      | addressLine2           | varchar    | YES         | NULL                  | NULL                   |
		| offices      | city                   | varchar    | NO          | NULL                  | NULL                   |
		| offices      | country                | varchar    | NO          | NULL                  | NULL                   |
		| offices      | officeCode             | varchar    | NO          | NULL                  | NULL                   |
		| offices      | phone                  | varchar    | NO          | NULL                  | NULL                   |
		| offices      | postalCode             | varchar    | NO          | NULL                  | NULL                   |
		| offices      | state                  | varchar    | YES         | NULL                  | NULL                   |
		| offices      | territory              | varchar    | NO          | NULL                  | NULL                   |
		| orderdetails | orderLineNumber        | smallint   | NO          | NULL                  | NULL                   |
		| orderdetails | orderNumber            | int        | NO          | NULL                  | NULL                   |
		| orderdetails | orderNumber            | int        | NO          | orders                | orderNumber            |
		| orderdetails | priceEach              | decimal    | NO          | NULL                  | NULL                   |
		| orderdetails | productCode            | varchar    | NO          | NULL                  | NULL                   |
		| orderdetails | productCode            | varchar    | NO          | products              | productCode            |
		| orderdetails | quantityOrdered        | int        | NO          | NULL                  | NULL                   |
		| orders       | comments               | text       | YES         | NULL                  | NULL                   |
		| orders       | customerNumber         | int        | NO          | customers             | customerNumber         |
		| orders       | orderDate              | date       | NO          | NULL                  | NULL                   |
		| orders       | orderNumber            | int        | NO          | NULL                  | NULL                   |
		| orders       | requiredDate           | date       | NO          | NULL                  | NULL                   |
		| orders       | shippedDate            | date       | YES         | NULL                  | NULL                   |
		| orders       | status                 | varchar    | NO          | NULL                  | NULL                   |
		| payments     | amount                 | decimal    | NO          | NULL                  | NULL                   |
		| payments     | checkNumber            | varchar    | NO          | NULL                  | NULL                   |
		| payments     | customerNumber         | int        | NO          | NULL                  | NULL                   |
		| payments     | customerNumber         | int        | NO          | customers             | customerNumber         |
		| payments     | paymentDate            | date       | NO          | NULL                  | NULL                   |
		| productlines | htmlDescription        | mediumtext | YES         | NULL                  | NULL                   |
		| productlines | image                  | mediumblob | YES         | NULL                  | NULL                   |
		| productlines | productLine            | varchar    | NO          | NULL                  | NULL                   |
		| productlines | textDescription        | varchar    | YES         | NULL                  | NULL                   |
		| products     | buyPrice               | decimal    | NO          | NULL                  | NULL                   |
		| products     | MSRP                   | decimal    | NO          | NULL                  | NULL                   |
		| products     | productCode            | varchar    | NO          | NULL                  | NULL                   |
		| products     | productDescription     | text       | NO          | NULL                  | NULL                   |
		| products     | productLine            | varchar    | NO          | productlines          | productLine            |
		| products     | productName            | varchar    | NO          | NULL                  | NULL                   |
		| products     | productScale           | varchar    | NO          | NULL                  | NULL                   |
		| products     | productVendor          | varchar    | NO          | NULL                  | NULL                   |
		| products     | quantityInStock        | smallint   | NO          | NULL                  | NULL                   |
		+--------------+------------------------+------------+-------------+-----------------------+------------------------+
		62 rows in set (0.219 sec)
    """,
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview",
)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
	role="assistant",
	content="Hello, I'm your new assistant. How can I help you?",
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
	assistant_id=assistant.id,
	instructions="""
		What are the top-selling items?
	""",
)

print(run.messages[0].content)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
	assistant_id=assistant.id,
	instructions="""
		Show me product reviews with 4 stars or above.
	""",
)

print(run.messages[0].content)

SSS