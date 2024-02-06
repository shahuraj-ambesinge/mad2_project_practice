import json
from flask import request, jsonify
from flask_restful import Resource, reqparse, abort, fields, marshal_with

from application.data.model import db, Book
print("this is me")
# instatiate object RequestParser(), define data in post method how it should be
book_post_args = reqparse.RequestParser()
book_post_args.add_argument('book_name', type=str)
book_post_args.add_argument('book_author', type=str)
book_post_args.add_argument('pages_in_book', type=int)
book_post_args.add_argument('price', type=int)

book_put_args = reqparse.RequestParser()
book_put_args.add_argument('book_name', type=str)
book_put_args.add_argument('book_author', type=str)
book_put_args.add_argument('pages_in_book', type=int)
book_put_args.add_argument('price', type=int)

#resource_fields is a dictionary used to define the structure and formatting of the response fields for a resource.
resource_fields = {
    'book_id': fields.Integer,
    'book_name': fields.String,
    'book_author': fields.String,
    'pages_in_book': fields.Integer,
    'price': fields.Integer,
}



class AllBookAPI(Resource):
    @marshal_with(resource_fields)
    def get(resources):
        books = Book.query.all()
        book_list = []
        for book in books:
            book_list.append({'book_id' : book.book_id, 'book_name' : book.book_name, 'book_author' : book.book_author})
        return book_list

    @marshal_with(resource_fields)
    def post(resources):
        args = book_post_args.parse_args()  #validating data in post request using reqparse before upload to database
        book = Book.query.filter_by(book_name = args["book_name"]).first()
        if book:
            return abort(409, message = "this book is already exit")
        input = Book(book_name = args["book_name"], book_author = args["book_author"], pages_in_book = args["pages_in_book"], price = args["price"])
        db.session.add(input)
        db.session.commit()
        return jsonify(message="Book is added in database successfuly")
    
    
#The @marshal_with(resource_fields) decorator takes care of converting the book object retrieved
#from the database into a dictionary with the specified structure defined in resource_fields
    
class BookAPI(Resource):
    @marshal_with(resource_fields)
    def get(self, book_id):
        get_book = Book.query.filter_by(book_id = book_id).first()
        return get_book

    @marshal_with(resource_fields)
    def put(self, book_id):
        args = book_put_args.parse_args()
        book = Book.query.filter_by(book_id = book_id).first()

        if not book:
            return abort(404, message = "this book is not in database")
        if args['book_name']:
            book.book_name = args['book_name']
        if args['book_author']:
            book.book_author = args['book_author']
        if args['pages_in_book']:
            book.pages_in_book = args['pages_in_book']
        if args['price']:
            book.price = args['price']
        db.session.commit()
        return book


    def delete(self, book_id):
        delete_book = Book.query.filter_by(book_id = book_id).first()
        db.session.delete(delete_book)
        db.session.commit()
        return jsonify("message:Book is deleted in database")
