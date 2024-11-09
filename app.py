from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
import pandas as pd
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/postgres'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = 'books'
    isbn = db.Column(db.String(13), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    short_description = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer)
    cover_url = db.Column(db.String(500))


def fetch_book_data(isbn):
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")
    if response.status_code == 200:
        book_data = response.json()
        if 'items' in book_data:
            book_info = book_data['items'][0]['volumeInfo']
            return {
                'isbn': isbn,
                'title': book_info.get('title', 'Unknown Title')[:255],
                'author': book_info.get('authors', ['Unknown Author'])[0][:255],
                'year': int(book_info.get('publishedDate', '0000')[:4]) if book_info.get('publishedDate', '0000')[
                                                                           :4].isdigit() else None,
                'short_description': book_info.get('description', 'No description available.')[:1000],
                'cover_url': book_info.get('imageLinks', {}).get('thumbnail', '')
            }
    return None


def add_books_bulk(isbns):
    books_to_add = []
    for isbn in isbns:
        book_data = fetch_book_data(isbn)
        if book_data:
            if not Book.query.get(isbn):
                books_to_add.append(Book(**book_data))
                print(f"Fetched data for ISBN {isbn}: {book_data['title']}")
            else:
                print(f"Book with ISBN {isbn} already exists.")

        time.sleep(0.1)

    if books_to_add:
        try:
            db.session.bulk_save_objects(books_to_add)
            db.session.commit()
            print(f"{len(books_to_add)} books added to the database.")
        except Exception as e:
            db.session.rollback()
            print(f"Failed to add books in bulk: {e}")
    else:
        print("No new books to add.")


def load_isbns_from_csv(file_path):
    df = pd.read_csv(file_path)
    isbns = df['ISBN13'].astype(str).tolist()
    return isbns


def initialize_database():
    with app.app_context():
        db.create_all()
        print("Database tables created.")

        isbns = load_isbns_from_csv('goodreads_dataset/isbns.csv')

        add_books_bulk(isbns)


@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([
        {
            'title': book.title,
            'isbn': book.isbn,
            'author': book.author,
            'year': book.year,
            'short_description': book.short_description,
            'cover_url': book.cover_url
        } for book in books
    ])


if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
