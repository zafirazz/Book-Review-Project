'''
    This python file implements functionality of the web application with a review function.
    It uses Flask framework for backend and SQLAlchemy for DB interactions.
'''

import logging
from functools import wraps
from flask import request, redirect, url_for, session, render_template, Flask, jsonify
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from models import Book, User_Data, Review

'''
    The application includes following functionalities:
        1. User authentication 
        2. Book searching and reviewing functionality
'''

#engine = create_engine('postgresql+psycopg2://username:password@localhost:5432/postgres')

app = Flask(__name__, template_folder='front-end', static_folder='front-end/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://@localhost:5432/postgres'
app.secret_key=["hioergerhgoierhgierhogiehgoieagawoeigyireyg"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

#Decorator that forces login (to review a book)
#https://flask.palletsprojects.com/en/stable/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('username') is None or session.get('logged_in') is None:
            logging.debug("i am in decorated function")
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function

'''
    There are following routes available:
        - '/front-end/login' -- User login.
        - '/front-end/register' -- User registration.
        - '/front-end/home' -- Home page of the application.
        - '/front-end/search' -- Search functionality to look for books based on keywords like title or author.
        - '/front-end/review' -- Review functionality.
        - '/front-end/book_page' -- List of available books.
        - '/front-end/read_review' -- Read review functionality.
        
'''

@app.route('/front-end/register', methods=['GET', 'POST'])
def register():
    '''
    Handles user registration.

    Methods:
        GET: Displays the registration form.
        POST: Validates user input, saves user data to the database, and redirects to the login page.

    Validation:
        - Username must not be empty or already taken.
        - Password and confirmation must match.

    :return:redirect to home page on successful registration. And error message on failure.
    '''
    logging.debug("I am in register function")
    session.clear()
    if request.method == 'POST':
        if not request.form.get("username"):
            return login_error("Username is required.", 400)
        if db.session.query(User_Data).filter_by(username= request.form.get("username")).first():
            return login_error("Username is already taken.", 400)
        if not request.form.get("password") and not request.form.get("password_confirm"):
            return login_error("Password and password confirmation is required.", 400)
        if request.form.get("password") != request.form.get("password_confirm"):
            return login_error("Password and password confirmation dont match.", 400)

        password = generate_password_hash(request.form.get("password"))
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        new_user = User_Data(username=request.form.get("username"), password=password, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        logging.debug("Added a new user to the table")
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


def login_error(message, code=400):
    '''
    Returns error message on failure of registration.
    :param message: text of the error.
    :param code: status code of the error.
    :return: rendered error message
    '''
    return render_template("login_error.html", top=code, bottom=message), code


@app.route('/front-end/login', methods=['GET', 'POST'])
def login():
    '''
    Handles user login.

    Methods:
        GET: Displays the login form.
        POST: Validates user credentials and sets session data on successful login.

    Validation:
        - Username and password must not be empty.
        - Password must match the hash stored in the database.

    :return:redirects to review page on successful login. And error message on failure.
    '''
    session.clear()
    logging.debug("I am in login function")
    if request.method == "POST":
        if not request.form.get("username"):
            return login_error("Please enter your username!", 401)
        elif not request.form.get("password"):
            return login_error("Please enter your password!", 401)
        username = request.form.get("username")
        password =request.form.get("password")
        user = db.session.query(User_Data).filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                logging.debug("password is correct")
                session['user_id'] = user.ID
                session['username'] = user.username
                logging.debug("User logged in")
                session['logged_in'] = True
                db.session.commit()
                return redirect(url_for('review'))
            else:
                logging.debug("password is invalid!")
        return login_error("invalid username or password", 401)

    return render_template('login.html')

@app.route('/front-end/home', methods=['GET', 'POST'])
def home():
    '''
    Displays list of available books on home page.
    :return:Renders the home page with a list of books fetched from the database.
    '''
    logging.debug("i am in review function")
    books = Book.query.all()
    return render_template('home.html', books=books)


@app.route('/front-end/search', methods=['GET', 'POST'])
def search():
    '''
    Handles book search functionality by title or author keywords.
    :return: Renders the search page with a list of found books.
    '''
    query = request.args.get('query', '').strip()
    results = []

    if query:
        results = Book.query.filter(
            (Book.title.ilike(f"%{query}%")) | (Book.author.ilike(f"%{query}%"))
        ).all()

    return render_template('search.html', query=query, results=results)


@app.route('/front-end/review', methods=['GET', 'POST'])
@login_required
def review():
    '''
    Handles book review functionality.
    :return: Renders the review submission page.
    '''
    logging.debug("i am in review function")
    books = Book.query.all()
    return render_template('review.html', books=books)


@app.route('/front-end/book_page',  methods=['GET', 'POST'])
def book_page():
    '''
    Displays details of a specific book and allows the user to submit a review.
    Args:
        - book (query parameter): The ISBN of the book.
    :return: Renders the book details and review form.
    '''
    book_isbn = request.args.get('book')
    username = session['username']
    userid = session['user_id']
    book = Book.query.filter_by(isbn=book_isbn).first()
    reviewed = db.session.query(Review).filter_by(isbn=book.isbn, user_id=userid).first()
    if not reviewed and request.method == "POST":
        review = request.form.get("review-written")
        if review:
            new_review = Review(isbn=book.isbn, user_id=userid, review=review)
            db.session.add(new_review)
            db.session.commit()
    if reviewed and request.method == "POST":
        #db.session.delete(reviewed)
        #db.session.commit()
        return login_error("you already reviewed this book", 401)
    return render_template('book_page.html', book=book, username=username)


@app.route('/front-end/read_review', methods=['GET', 'POST'])
def read_review():
    logging.debug("i am in review function")
    books = Book.query.all()
    return render_template('read_review.html', books=books)


@app.route('/front-end/read_reviews', methods=['GET', 'POST'])
def read_reviews():
   book_isbn = request.args.get('book')
   book = Book.query.filter_by(isbn=book_isbn).first()
   reviews = db.session.query(Review, User_Data).join(User_Data, Review.user_id == User_Data.ID).filter(Review.isbn==book_isbn).all()
   return render_template('read_reviews.html', book=book, reviews=reviews)

def initialize_database():
    '''
    Initializes the database by creating the required tables.

    This function runs before starting the server.
    :return: created DB
    '''
    with app.app_context():
        db.create_all()
        print("Database tables for user data created.")


def main():
    initialize_database()
    app.run(debug=True)


if __name__ == '__main__':
    main()
