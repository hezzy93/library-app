from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base, get_db
import crud, models, schema
from typing import List
#from rabbitmq import publish_book_update, consume_book_updates
import threading
from rabbitmq import consume_messages, publish_message
import json

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
consumer_thread = None




def start_consumer():
    consume_messages()

@app.on_event("startup")
def startup_event():
    global consumer_thread
    consumer_thread = threading.Thread(target=start_consumer)
    consumer_thread.start()

@app.on_event("shutdown")
def shutdown_event():
    if consumer_thread is not None:
        consumer_thread.join()  # Wait for the thread to finish

@app.post("/books/", tags=["Admin"])
def create_book(book: schema.BookCreate, db: Session = Depends(get_db)):
    added_book = crud.add_book(db=db, book=book)
    return {
        "message": "Book added successfully",
        "book": added_book
    }


# Endpoint to DELETE a book by Id
@app.delete("/books/{book_id}", response_model=dict, tags=["Books"])
def delete_book(book_id: int, db: Session = Depends(get_db)):
    result = crud.delete_book(db, book_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])

    # Publish a message to RabbitMQ about the deleted book
    book_message = {
        "book_id": book_id,
        "action": "delete"
    }
    publish_message(book_message)  # Send book deletion message to RabbitMQ
    return result

# # Endpoint to delete a book
# @app.delete("/Delete_Book/{book_id}", tags=["Backend API"])
# def delete_book(book_id: int, db: Session = Depends(get_db)):
#     book = crud.get_book(db, book_id=book_id)
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")
    
#     crud.delete_book(db=db, book=book)
    
#     # Publish a message to RabbitMQ to notify the frontend about the deletion
#     book_message = {
#         "book_id": book.id,
#         "action": "delete"
#     }
#     publish_message(book_message)  # Send the book deletion data to RabbitMQ
    
#     return {"message": "Book deleted successfully"}

# Endpoint to GET all users
@app.get("/users/", response_model=List[schema.User], tags=["Users"])
def get_users(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    users = crud.get_users(db, offset=offset, limit=limit)
    return users

# Endpoint to fetch/list the books that are not available for borrowing
@app.get("/books/unavailable", response_model=List[schema.BookUnavailable], tags=["Books"])
def get_unavailable_books(db: Session = Depends(get_db)):
    unavailable_books = crud.get_unavailable_books(db)
    
    if not unavailable_books:
        raise HTTPException(status_code=404, detail="No unavailable books found")
    
    return unavailable_books



@app.get("/books/", response_model=List[schema.Book], tags=["Books"])
def get_books(db: Session = Depends(get_db), offset: int = 0, limit: int = 10):
    books = crud.get_books(db, offset=offset, limit=limit)
    return books


@app.get("/")
def read_root():
    return {"Hello": "World"}
