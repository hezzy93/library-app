from sqlalchemy import Boolean, Column, Date ,ForeignKey, Integer, String
from sqlalchemy.orm import relationship


from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    first_name = Column(String, index=True, nullable=False)

    # Relationship with books
    books = relationship("Book", back_populates="user", cascade="all, delete-orphan")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    publisher = Column(String(100), index=True, nullable=False)
    category = Column(String(100), index=True, nullable=False)
    available = Column(Boolean, index=True, default=True, nullable=False)
    borrow_date = Column(Date, nullable=True)
    return_date = Column(Date, nullable=True)
    borrower_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    

    # Relationship with user (borrower)
    user = relationship("User", back_populates="books")