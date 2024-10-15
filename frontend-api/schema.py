from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date

# User Schema
class UserBase(BaseModel):
    email: str
    firstname: str
    lastname: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Book Schema
class BookBase(BaseModel):
    title: str
    publisher: str
    category: str
    available: bool
    borrower_id: Optional[int] = None  # ID of the user who borrowed the book
    borrow_date: Optional[date] = None  # Date when the book was borrowed
    return_date: Optional[date] = None  # Date when the book is due to be returned

    model_config = ConfigDict(from_attributes=True)


class Book(BookBase):
    id: int

    # Relationship with user who borrowed the book
    borrower_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class BookBorrow(BaseModel):
    book_id: int  # Identify the book to borrow by ID
    borrow_duration: int

class BorrowedBookResponse(BaseModel):
    book_title: str
    borrow_date: date
    return_date: date
    user_email: str

    model_config = ConfigDict(from_attributes=True)


# Book schema for creating new books
class BookCreate(BaseModel):
    id: Optional[int] = None
    title: str
    publisher: str
    category: str
    available: bool = True

    model_config = ConfigDict(from_attributes=True)
