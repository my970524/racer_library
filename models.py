from db_connect import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"
    email = db.Column(
            db.String(320), 
            primary_key=True, 
            nullable=False, 
            unique=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password


class Book(db.Model):
    __tablename__= "book"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=True)
    title = db.Column(db.String(100), nullable=True)
    author = db.Column(db.String(100), nullable=True)
    publisher = db.Column(db.String(100), nullable=True)
    release_date = db.Column(db.Date, nullable=True)
    pages = db.Column(db.BigInteger, nullable= True)
    isbn_code = db.Column(db.String(100), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    introduction = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(500), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
        
    def __init__(self, title, author, publisher, release_date, pages, isbn_code, quantity, introduction, description, rating):
        self.title = title
        self.author = author
        self.publisher = publisher
        self.release_date = release_date
        self.pages = pages
        self.isbn_code = isbn_code
        self.quantity = quantity
        self.introduction = introduction
        self.description= description
        self.rating = 0

class User_Book(db.Model):
    __tablename__ = "user_book"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_email = db.Column(db.String(320), db.ForeignKey('user.email'), nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=True)
    book_title = db.Column(db.String(100), nullable=True)

    def __init__(self, user_email, book_id, book_title):
        self.user_email = user_email
        self.book_id = book_id
        self.book_title = book_title

class Review(db.Model):
    __tablename__ = "review"
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_email = db.Column(db.String(320), db.ForeignKey('user.email'), nullable=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    content = db.Column(db.Text())
    posted_at = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, user_email, book_id, rating, content):
        self.user_email = user_email
        self.book_id = book_id
        self.rating = rating
        self.content = content