from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date


# Schema for creating new books
class BookCreate(BaseModel):
    title: str
    publisher: str
    category: str
    available: bool = True

    model_config = ConfigDict(from_attributes=True)


# Schema for updating book details
class BookUpdate(BaseModel):
    title: Optional[str] = None
    publisher: Optional[str] = None
    category: Optional[str] = None
    available: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


# Schema for book response including borrow information
class Book(BaseModel):
    id: int
    title: str
    publisher: str
    category: str
    available: bool
    borrower_id: Optional[int] = None  # ID of the user who borrowed the book
    borrow_date: Optional[date] = None  # Date when the book was borrowed
    return_date: Optional[date] = None  # Date when the book is due to be returned

    model_config = ConfigDict(from_attributes=True)


# Schema for borrowing a book
class BookBorrow(BaseModel):
    book_id: int  # ID of the book to borrow
    borrow_duration: int  # Number of days the book will be borrowed for

    model_config = ConfigDict(from_attributes=True)


# Schema for returning a book
class BookReturn(BaseModel):
    book_id: int  # ID of the book to return

    model_config = ConfigDict(from_attributes=True)


# Schema for displaying books borrowed by a user
class BookBorrowed(BaseModel):
    id: int
    title: str
    publisher: str
    category: str
    borrow_date: Optional[date] = None
    return_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


# Extend the User schema to include borrowed books
class UserWithBorrowedBooks(BaseModel):
    id: int
    email: str
    firstname: str
    lastname: str
    borrowed_books: List[BookBorrowed]  # List of books the user has borrowed

    model_config = ConfigDict(from_attributes=True)


# Schema for displaying books that are currently unavailable (borrowed)
class BookUnavailable(BaseModel):
    id: int
    title: str
    publisher: str
    category: str
    return_date: Optional[date] = None  # When the book will be available

    model_config = ConfigDict(from_attributes=True)


# Schema for user-related operations in the backend
class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str

class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
