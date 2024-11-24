"""first: get login data from login.html
second: create database containing id, username, password and review
third: add username, password to the database"""
import logging
from functools import wraps
from flask import g, request, redirect, url_for, session, render_template, Flask, jsonify
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash

from db import db
from models import Book, User_Data


engine = create_engine('postgresql://localhost:5432/postgres')

app = Flask(__name__, template_folder='front-end', static_folder='front-end/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/postgres'
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


@app.route('/front-end/register', methods=['GET', 'POST'])
def register():
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
    return render_template("login_error.html", top=code, bottom=message), code


@app.route('/front-end/login', methods=['GET', 'POST'])
def login():
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
    return render_template('home.html')


@app.route('/front-end/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query', '').strip()
    results = []

    if query:
        results = Book.query.filter(
            (Book.title.ilike(f"%{query}%")) | (Book.author.ilike(f"%{query}%"))
        ).all()

    return render_template('search.html', query=query, results=results)


@app.route('/front-end/logout', methods=['GET', 'POST'])
def logout():
    # TODO
    return 0

@app.route('/front-end/review', methods=['GET', 'POST'])

@login_required
def review():
    logging.debug("i am in review function")
    books = Book.query.all()
    return render_template('review.html', books=books)


def initialize_database():
    with app.app_context():
        db.create_all()
        print("Database tables for user data created.")


def main():
    initialize_database()
    app.run(debug=True)


if __name__ == '__main__':
    main()