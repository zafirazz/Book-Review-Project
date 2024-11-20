
from flask import render_template, Flask

from app import Book, app

app = Flask(__name__, template_folder='front-end', static_folder='front-end/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/front-end/review', methods = ['GET', 'POST'])
def display_books():
    books = Book.query.all()
    return render_template('review.html', books=books)

if __name__ == '__main__':
    app.run(debug=True, port=5001)