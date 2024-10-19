
import pika

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Acknowledge the message

def consume_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    
    channel.queue_declare(queue='hello')  # Ensure the queue exists

    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()



import pika
import json  # To convert Python dictionary to JSON

def publish_message(message: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='book_updates')
    # Convert the message (book data) to JSON before sending
    channel.basic_publish(exchange='', routing_key='book_updates', body=json.dumps(message))
    print(f" [x] Sent '{message}'")
    connection.close()


import pika
import json
import crud
from database import SessionLocal
import schema  # Import the schema for UserCreate

# def callback(ch, method, properties, body):
#     message = json.loads(body.decode())
#     print(f" [x] Received {message}")

#     # Create a UserCreate object from the received message
#     user_create = schema.UserCreate(
#         email=message['email'],
#         first_name=message['first_name'],
#         last_name=message['last_name']
#     )

#     # Insert the received user into the backend database
#     db = SessionLocal()
#     crud.create_user(db=db, user=user_create)
#     added_user = crud.create_user(db=db, user=user_create)
#     print(f" [x] User added to frontend database: {added_user}")
#     db.close()

#     ch.basic_ack(delivery_tag=method.delivery_tag)


def callback(ch, method, properties, body):
    try:
        message = json.loads(body.decode())
        print(f" [x] Received {message}")

        user_create = schema.UserCreate(
            email=message['email'],
            first_name=message['first_name'],
            last_name=message['last_name']
        )

        db = SessionLocal()
        added_user = crud.create_user(db=db, user=user_create)
        print(f" [x] User added to backend database: {added_user}")
        db.close()

        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f" [!] Error processing message: {e}")


def consume_messages():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='user_updates')

    print(' [*] Backend waiting for messages on user_updates queue...')  # Debug log

    channel.basic_consume(queue='user_updates', on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for user updates. To exit press CTRL+C')
    channel.start_consuming()





