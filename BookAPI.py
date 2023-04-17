# Ashton Wood 
# 04-16-2023
# BookAPI
# python to manage a api for books


from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/books-api'
mongo = PyMongo(app)

# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    book = mongo.db.books.insert_one(request.json)
    new_book = mongo.db.books.find_one({'_id': book.inserted_id})
    return jsonify({'message': 'Book created', 'book': new_book})

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = list(mongo.db.books.find())
    return jsonify(books)

# Get a book by id
@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    book = mongo.db.books.find_one({'_id': id})
    if book:
        return jsonify(book)
    else:
        return jsonify({'message': 'Book not found'})

# Update a book by id
@app.route('/books/<id>', methods=['PATCH'])
def update_book(id):
    mongo.db.books.update_one({'_id': id}, {'$set': request.json})
    book = mongo.db.books.find_one({'_id': id})
    if book:
        return jsonify({'message': 'Book updated', 'book': book})
    else:
        return jsonify({'message': 'Book not found'})

# Delete a book by id
@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = mongo.db.books.find_one({'_id': id})
    if book:
        mongo.db.books.delete_one({'_id': id})
        return jsonify({'message': 'Book deleted', 'book': book})
    else:
        return jsonify({'message': 'Book not found'})

if __name__ == '__main__':
    app.run(debug=True)

