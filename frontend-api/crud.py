from sqlalchemy.orm import Session
import models
import schema
from sqlalchemy import func
from fastapi import HTTPException
from datetime import date, timedelta

# Create User
def create_user(db: Session, user: schema.UserCreate):
    db_user = models.User(
        email=user.email,
        last_name=user.lastname,
        first_name=user.firstname
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user    

# Get User by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email.ilike(email)).first()

# # Borrow Book
# def borrow_book(db: Session, book_borrow: schema.BookBorrow, user_id: int):
#     db_book = db.query(models.Book).filter(models.Book.id == book_borrow.book_id).first()
    
#     if not db_book:
#         raise HTTPException(status_code=404, detail="Book not found")
    
#     if not db_book.available:
#         raise HTTPException(status_code=400, detail="Book is not available")
    
#     db_book.available = False
#     db_book.borrower_id = user_id
#     db_book.borrow_date = date.today()
#     db_book.return_date = date.today() + timedelta(days=book_borrow.borrow_duration)

#     db.commit()
#     db.refresh(db_book)

#     return db_book


# Borrow Book
def borrow_book(db: Session, book_borrow: schema.BookBorrow, user_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_borrow.book_id).first()
    
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if not db_book.available:
        raise HTTPException(status_code=400, detail="Book is not available")
    
    db_book.available = False
    db_book.borrower_id = user_id
    db_book.borrow_date = date.today()
    db_book.return_date = date.today() + timedelta(days=book_borrow.borrow_duration)

    db.commit()
    db.refresh(db_book)



    return db_book

# Get all books
def get_books(db: Session, offset: int = 0, limit: int = 10):

    return db.query(models.Book).offset(offset).limit(limit).all()

# Get book by id
def get_book_by_id(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

# Filter books by publisher
def filter_book_publisher(db: Session, publisher: str):
    return db.query(models.Book).filter(models.Book.publisher == publisher).all()

# Filter books by category
def filter_book_category(db: Session, category: str):
    return db.query(models.Book).filter(models.Book.category == category).all()

# # Add Book
# def add_book(db: Session, book: schema.BookCreate):
#     db_book = models.Book(**book.dict())
#     db.add(db_book)
#     db.commit()
#     db.refresh(db_book)
#     return db_book

def add_book(db: Session, book: schema.BookCreate):
    db_book = models.Book(
        id=book.id,  # Use the id passed from the message
        title=book.title,
        publisher=book.publisher,
        category=book.category,
        available=book.available
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# Frontend's CRUD to delete a book
def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()

    if db_book:
        db.delete(db_book)
        db.commit()
        print(f" [x] Deleted book with ID {book_id} from the frontend database")
    else:
        print(f" [!] Book with ID {book_id} not found in the frontend database")
