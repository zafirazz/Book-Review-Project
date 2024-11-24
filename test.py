from flask import jsonify, request, Flask

from models import Book

app = Flask(__name__)

@app.route('/debug-query')
def debug_query():
    query = request.args.get('query', '')
    if not query:
        return {"error": "No query provided"}

    # Perform the database query
    results = Book.query.filter(Book.title.ilike(f"%{query}%")).all()

    # Log the results to ensure the query works
    for book in results:
        print(f"Found: {book.title} by {book.author}")

    # Return the results as JSON for easy debugging
    return jsonify([
        {"id": book.isbn, "title": book.title, "author": book.author}
        for book in results
    ])

if __name__ == '__main__':
    app.run(debug=True)