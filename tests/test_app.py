
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from api import create_app
from api.model.model import setup_db, db, Category, Book
from random import randint

ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN')
USER_TOKEN = os.environ.get('USER_TOKEN')


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # create app - api.py
        self.app = create_app()
        self.client = self.app.test_client
        self.admin_jwt = {
            "Authorization": f"Bearer {ADMIN_TOKEN}"
        }
        self.user_jwt = {
            "Authorization": f"Bearer {USER_TOKEN}"
        }
        # create db - model.py & binds the app to the current context
        with self.app.app_context():
            self.database_path = "postgresql://{}:{}@{}/{}".format(
                'admin', 'admin', 'localhost:5432', "library_test")
            setup_db(self.app, self.database_path)
            db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        self.delete_data()

    def delete_data(self):
        with self.app.app_context():
            books = Book.query.all()
            for book in books:
                book.delete()
            categories = Category.query.all()
            for category in categories:
                category.delete()

    def add_book(self):
        with self.app.app_context():
            # add new demo data into postgres
            random_id = randint(1000000, 9999999)
            new_book = Book(name=f"Test_Book_{random_id}")
            new_book.category = self.add_category()
            new_book.insert()
            return new_book

    def add_category(self):
        with self.app.app_context():
            # add new demo data into postgres
            random_id = randint(1000000, 9999999)
            new_category = Category(name=f"Test_Category_{random_id}")
            new_category.insert()
            return new_category

    # GET /books
    # success
    def test_200_get_books(self):
        new_book = self.add_book()
        header = self.user_jwt
        res = self.client().get('/books', headers=header)
        self.assertEqual(res.status_code, 200)

    # failure
    def test_422_get_books(self):
        self.delete_data()
        header = self.admin_jwt
        res = self.client().get('/books', headers=header)
        self.assertEqual(res.status_code, 422)

    # GET /categories
    # success
    def test_200_get_categories(self):
        new_category = self.add_category()
        header = self.admin_jwt
        res = self.client().get('/categories', headers=header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    # failure

    def test_422_get_categories(self):
        self.delete_data()
        header = self.admin_jwt
        res = self.client().get('/categories', headers=header)
        self.assertEqual(res.status_code, 422)

    # POST /books
    def test_200_POST_books(self):
        new_book = self.add_book()
        header = self.user_jwt
        res = self.client().post('/books', headers=header)
        self.assertEqual(res.status_code, 200)

# def test_404_sent_requesting_beyond_valid_page(self):
#     res = self.client().get('/books?page=1000', json={'rating': 1})
#     data = json.loads(res.data)
#
#     self.assertEqual(res.status_code, 404)
#     self.assertEqual(data['success'], False)
#     self.assertEqual(data['message'], 'resource not found')

# def test_post(self):
#     res = self.client().post('/books', json={'title':'test_title','author':'test_author','rating': 1})
#     data = json.loads(res.data)
#     self.assertEqual(res.status_code, 200)
#     self.assertEqual(data['success'], True)
#     self.assertTrue(data['created'])

# def test_post_with_search(self):
#     response = self.client().post('/books/search',json={'title':'test4_search_title','author':'test4_search_uthor','rating': 1})
#     data = json.loads(response.data)
#     new_book = Book.query.filter_by(id=data['new_book_id']).first()
#     self.assertEqual(response.status_code, 200)
#     self.assertEqual(data['success'], True)
#     self.assertEqual(data['new_book'], new_book.format())
#     self.assertEqual(data['total_books'],len(Book.query.all()))


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite)
    # unittest.main()
