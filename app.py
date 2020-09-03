import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from model.model import setup_db, db, Book, Category
from auth.auth import AuthError, requires_auth, get_token_auth_header
import json


def create_app():
    app = Flask(__name__)
    # model.setup_db
    setup_db(app)
    CORS(app)

    @app.route('/healthy')
    def health():
        return jsonify({"code": 200, "msg": "healthy"})
    # GET endpoints

    @app.route('/books', methods=['GET'])
    @requires_auth('get:books')
    def get_books(payload):
        books = Book.query.order_by(Book.name).all()
        books_list = [book.format() for book in books]
        if len(books) == 0:
            abort(422)
        return jsonify({'success': True,
                        'books': books_list,
                        'total_books': len(books)})

    @app.route('/categories', methods=['GET'])
    @requires_auth('get:books')
    def get_categories(payload):
        categories = Category.query.order_by(Category.name).all()
        categories_list = [category.format() for category in categories]
        if len(categories_list) == 0:
            abort(422)
        return jsonify({'success': True,
                        'categories': categories_list,
                        'total_categories': len(categories)})

    # POST endpoints

    @app.route('/books', methods=['POST'])
    @requires_auth('post:books')
    def post_book(payload):
        body = request.get_json()
        book_name = body.get('name', None)
        book_category_name = body.get("category", None)
        if book_name:
            new_book = Book(name=book_name)
            if book_category_name:
                category = Category.query.filter(Category.name == book_category_name).first()
                if category:
                    new_book.category = category
                else:
                    abort(422)
            try:
                new_book.insert()
            except:
                abort(500)
        else:
            abort(422)

        return jsonify({'success': True,
                        'id': new_book.id,
                        "name": new_book.name})

    @app.route('/categories', methods=['POST'])
    @requires_auth('post:categories')
    def post_category(payload):
        body = request.get_json()
        category_name = body.get('name', None)
        if category_name:
            existed_category = Category.query.filter(
                Category.name == category_name).first()
            if existed_category:
                abort(409)
            else:
                try:
                    new_category = Category(name=category_name)
                    new_category.insert()
                except:
                    abort(500)
        else:
            abort(422)
        return jsonify({'success': True,
                        'id': new_category.id,
                        "name": new_category.name})

    # Delete endpoints

    @app.route('/books', methods=["DELETE"])
    @requires_auth('delete:books')
    def delete_book(payload):
        body = request.get_json()
        book_name = body.get("name", None)
        book_id = body.get("id", None)
        if (not book_name) and (not book_id):
            abort(422)
        else:
            if book_name:
                books_to_delete = Book.query.filter(Book.name == book_name).all()
                if books_to_delete:
                    try:
                        for book in books_to_delete:
                            book.delete()
                            return jsonify({'success': True,
                                            "book_name_deleted": book_name})
                    except:
                        abort(422)
                else:
                    abort(422)
            if book_id:
                book_to_delete = Book.query.filter(Book.id == book_id).first()
                try:
                    book_to_delete.delete()
                    return jsonify({'success': True,
                                    "book_id_deleted": book_id})
                except:
                    abort(422)

    # PATCH endpoints

    @app.route('/books/<int:book_id>', methods=["PATCH"])
    @requires_auth('patch:books')
    def patch_book(payload, book_id):
        body = request.get_json()
        book_to_update = Book.query.filter(Book.id == book_id).one_or_none()
        new_name = body.get("name", None)
        new_category = Category.query.filter(Category.name == body.get("category", None)).first()
        if not book_to_update:
            abort(404)
        else:
            try:
                if not(new_name) and not(new_category):
                    print("all body is not valid")
                    abort(422)
                elif not(new_name):  # new_name == None
                    print("new_name == None")
                    print(new_category)
                    book_to_update.category = new_category
                    book_to_update.update()
                elif not(new_category):  # new_category == None
                    print("new_category == None")
                    print(new_name)
                    book_to_update.name = new_name
                    book_to_update.update()
                else:  # new_name + new_cateogry !=  None
                    print("new_name + new_cateogry !=  None")
                    book_to_update.category = new_category
                    book_to_update.name = new_name
                    book_to_update.update()
            except:
                abort(400)

        return jsonify({'success': True,
                        "book_id_updated": book_id})

    @app.errorhandler(400)
    def error_400(error):
        return jsonify({"success": False, "message": "bad request"}), 400

    @app.errorhandler(404)
    def error_404(error):
        return jsonify({"success": False, "message": "page not found"}), 404

    @app.errorhandler(422)
    def error_422(error):
        return jsonify({"success": False, "message": "resource not found"}), 422

    @app.errorhandler(409)
    def error_409(error):
        return jsonify({"success": False, "message": "conflict resources"}), 409

    @app.errorhandler(500)
    def error_500(error):
        return jsonify({"success": False, "message": "internal server error. ex: db failure"}), 500

    @app.errorhandler(AuthError)
    def Auth_Error(auth_error):
        return jsonify({
            'error': auth_error.status_code,
            'success': False,
            'message': auth_error.error
        }), auth_error.status_code

    return app
