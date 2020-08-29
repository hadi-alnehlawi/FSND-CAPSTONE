
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import create_app


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "library_test"
        self.database_path = "postgres://{}:{}@{}/{}".format('admin', 'admin','localhost:5432', self.database_name)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
#
#         self.new_book = {
#             'title': 'Anansi Boys',
#             'author': 'Neil Gaiman',
#             'rating': 5
#         }
#
#         # binds the app to the current context
#         with self.app.app_context():
#             self.db = SQLAlchemy()
#             self.db.init_app(self.app)
#             # create all tables
#             self.db.create_all()
#
#     def tearDown(self):
#         """Executed after reach test"""
#         pass
#
# # @TODO: Write at least two tests for each endpoint - one each for success and error behavior.
# #        You can feel free to write additional tests for nuanced functionality,
# #        Such as adding a book without a rating, etc.
# #        Since there are four routes currently, you should have at least eight tests.
# # Optional: Update the book information in setUp to make the test database your own!
#
#
#     def test_get_paginated_books(self):
#         res = self.client().get('/books')
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertTrue(data['total_books'])
#         self.assertTrue(len(data['books']))
#
#     def test_404_sent_requesting_beyond_valid_page(self):
#         res = self.client().get('/books?page=1000', json={'rating': 1})
#         data = json.loads(res.data)
#
#         self.assertEqual(res.status_code, 404)
#         self.assertEqual(data['success'], False)
#         self.assertEqual(data['message'], 'resource not found')
#
#     # def test_post(self):
#     #     res = self.client().post('/books', json={'title':'test_title','author':'test_author','rating': 1})
#     #     data = json.loads(res.data)
#     #     self.assertEqual(res.status_code, 200)
#     #     self.assertEqual(data['success'], True)
#     #     self.assertTrue(data['created'])
#
#     def test_post_with_search(self):
#         response = self.client().post('/books/search',json={'title':'test4_search_title','author':'test4_search_uthor','rating': 1})
#         data = json.loads(response.data)
#         new_book = Book.query.filter_by(id=data['new_book_id']).first()
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(data['success'], True)
#         self.assertEqual(data['new_book'], new_book.format())
#         self.assertEqual(data['total_books'],len(Book.query.all()))



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite)
