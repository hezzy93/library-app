from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base, get_db
import crud, models, schema
from typing import List
import threading
import json
#from rabbitmq import consume_book_updates, handle_message
#from rabbitmq import consume_messages, publish_message
from rabbitmq import consume_book_updates, publish_message


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()



# Background thread to consume RabbitMQ messages
# consumer_thread = threading.Thread(target=consume_messages)
# consumer_thread.start()

consumer_thread = threading.Thread(target=consume_book_updates)
consumer_thread.start()


@app.post("/send/")
def send_message(message: str):
    publish_message(message)
    return {"message": "Message sent!"}


# # Endpoint to Enroll new user
# @app.post("/Enroll_User/", tags=["Frontend API"])
# def enroll(user: schema.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")
    
#     created_user = crud.create_user(db=db, user=user)
#     return {"message": "Account created successfully", 
#             "user": created_user}

# Endpoint to Enroll new user
@app.post("/Enroll_User/", tags=["Frontend API"])
def enroll(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    created_user = crud.create_user(db=db, user=user)
    
    # Publish the user data to RabbitMQ for the backend to consume
    user_message = {
        "email": created_user.email,
        "first_name": created_user.first_name,
        "last_name": created_user.last_name
    }
    publish_message(user_message)  # Send the user data to RabbitMQ

    return {"message": "Account created successfully", "user": created_user}

# Endpoint to borrow book
@app.post("/books/borrow", response_model=schema.BorrowedBookResponse, tags=["Books"])
def borrow_book(email: str, book_borrow: schema.BookBorrow, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(status_code=400, detail="Email not registered")

    borrowed_book = crud.borrow_book(db=db, book_borrow=book_borrow, user_id=db_user.id)
    
    return schema.BorrowedBookResponse(
        book_title=borrowed_book.title,
        borrow_date=borrowed_book.borrow_date,
        return_date=borrowed_book.return_date,
        user_email=db_user.email
    )

# Endpoint to GET all books
@app.get("/books/", response_model=List[schema.Book], tags=["Books"])
def get_books(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    books = crud.get_books(db, offset=offset, limit=limit)
    return books

# Endpoint to get a book by id
@app.get("/books/{book_id}", response_model=schema.Book, tags=["Books"])
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# Endpoint to get books by publisher
@app.get("/books/publisher/{publisher}", response_model=List[schema.Book], tags=["Books"])
def filter_book_publisher(publisher: str, db: Session = Depends(get_db)):
    db_books = crud.filter_book_publisher(db, publisher)
    if not db_books:
        raise HTTPException(status_code=404, detail="No books found for this publisher")
    return db_books

# Endpoint to get books by category
@app.get("/books/category/{category}", response_model=List[schema.Book], tags=["Books"])
def filter_book_category(category: str, db: Session = Depends(get_db)):
    db_books = crud.filter_book_category(db, category)
    if not db_books:
        raise HTTPException(status_code=404, detail="No books found for this category")
    return db_books

@app.get("/")
def read_root():
    return {"Hello": "World"}



    # To remove later

# Endpoint to DELETE a book by Id
@app.delete("/books/{book_id}", response_model=dict, tags=["Books"])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    result = crud.delete_book(db, book_id)
    return result
