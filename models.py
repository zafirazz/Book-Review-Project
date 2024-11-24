from sqlalchemy.orm import relationship

from db import db

class User_Data(db.Model):
    __tablename__ = 'User_Data'
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)

class Book(db.Model):
    __tablename__ = 'books'
    isbn = db.Column(db.String(13), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer)
    cover_url = db.Column(db.String(500))

class Review(db.Model):
    __tablename__ = 'Review'
    isbn = db.Column(db.String(13), db.ForeignKey('books.isbn'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User_Data.ID'), primary_key=True)
    review = db.Column(db.Text, nullable=False)

    user = relationship('User_Data', backref='reviews')
    book = relationship('Book', backref='reviews')
