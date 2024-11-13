from flask import render_template

from app import Book, app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/review', methods = ['GET', 'POST'])
def display_books():
    books = Book.query.all()
    return render_template('review.html', books=books)

if __name__ == '__main__':
    app.run(debug=True, port=5001)