
import pika

def publish_message(message: str):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body=message)
    print(f" [x] Sent '{message}'")
    connection.close()

import pika
import json
import crud
from database import SessionLocal
import schema  # Import the schema for BookCreate

# def callback(ch, method, properties, body):
#     message = json.loads(body.decode())
#     print(f" [x] Received {message}")

#     # Create a BookCreate object from the received message
#     book_create = schema.BookCreate(
#         title=message['title'],
#         publisher=message['publisher'],
#         category=message['category'],
#         available= message['available']
#     )

#     # Insert the received book into the frontend database
#     db = SessionLocal()
#     # crud.add_book(db=db, book=book_create)  # Pass the BookCreate object to add_book
#     added_book = crud.add_book(db=db, book=book_create)
#     print(f" [x] Book added to frontend database: {added_book}")
#     db.close()

#     ch.basic_ack(delivery_tag=method.delivery_tag)

# def consume_messages():
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
#     channel = connection.channel()

#     channel.queue_declare(queue='book_updates')
#     channel.basic_consume(queue='book_updates', on_message_callback=callback, auto_ack=False)

#     print(' [*] Waiting for book updates. To exit press CTRL+C')
#     channel.start_consuming()


# #TO Delete book

# def delete_book_callback(ch, method, properties, body):
#     message = json.loads(body.decode())
#     print(f" [x] Received {message}")

#     if message.get("action") == "delete":
#         book_id = message.get("book_id")
#         if book_id:
#             # Delete the book from the frontend database
#             db = SessionLocal()
#             crud.delete_book(db=db, book_id=book_id)  # Call the frontend's delete function
#             db.close()
    
#     ch.basic_ack(delivery_tag=method.delivery_tag)

# def consume_messages():
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
#     channel = connection.channel()

#     channel.queue_declare(queue='book_updates')
#     channel.basic_consume(queue='book_updates', on_message_callback=callback, auto_ack=False)

#     print(' [*] Waiting for book updates. To exit press CTRL+C')
#     channel.start_consuming()



# def callback(ch, method, properties, body):
#     message = json.loads(body.decode())
#     print(f" [x] Received {message}")

#     # Check if the message is for deletion or addition
#     if message.get("action") == "delete":
#         # Delete book
#         book_id = message.get("book_id")
#         if book_id:
#             # Delete the book from the frontend database
#             db = SessionLocal()
#             crud.delete_book(db=db, book_id=book_id)
#             print(f" [x] Deleted book with ID {book_id} from frontend database")
#             db.close()
#         else:
#             print(" [!] 'book_id' not found in the message for deletion.")
#     else:
#         # Add book
#         try:
#             book_create = schema.BookCreate(
#                 title=message['title'],
#                 publisher=message['publisher'],
#                 category=message['category'],
#                 available=message['available']
#             )

#             # Insert the received book into the frontend database
#             db = SessionLocal()
#             added_book = crud.add_book(db=db, book=book_create)
#             print(f" [x] Book added to frontend database: {added_book.title}")
#             db.close()
#         except KeyError as e:
#             print(f" [!] Missing field in message: {str(e)}")

#     ch.basic_ack(delivery_tag=method.delivery_tag)



# def publish_message(message: dict):
#     connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
#     channel = connection.channel()

#     channel.queue_declare(queue='user_updates')
#     channel.basic_publish(exchange='', routing_key='user_updates', body=json.dumps(message))
#     print(f" [x] Sent '{message}'")
#     connection.close()


# Publish message to RabbitMQ
def publish_message(message: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='user_updates')
    channel.basic_publish(exchange='', routing_key='user_updates', body=json.dumps(message))
    print(f" [x] Sent '{message}'")
    connection.close()

# Callback for receiving messages (add or delete a book)
def callback(ch, method, properties, body):
    message = json.loads(body.decode())
    print(f" [x] Received {message}")

    # Check if the message is for deletion or addition
    if message.get("action") == "delete":
        # Delete book
        book_id = message.get("book_id")
        if book_id:
            db = SessionLocal()
            crud.delete_book(db=db, book_id=book_id)
            print(f" [x] Deleted book with ID {book_id} from frontend database")
            db.close()
        else:
            print(" [!] 'book_id' not found in the message for deletion.")
    else:
        # Add book
        try:
            book_create = schema.BookCreate(
                id=message['id'],  # Set the same id as the backend
                title=message['title'],
                publisher=message['publisher'],
                category=message['category'],
                available=message['available']
            )

            db = SessionLocal()
            added_book = crud.add_book(db=db, book=book_create)
            print(f" [x] Book added to frontend database: {added_book.title}")
            db.close()
        except KeyError as e:
            print(f" [!] Missing field in message: {str(e)}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

# Function to consume book updates from RabbitMQ
def consume_book_updates():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='book_updates')
    channel.basic_consume(queue='book_updates', on_message_callback=callback, auto_ack=False)

    print(' [*] Waiting for book updates. To exit press CTRL+C')
    channel.start_consuming()
