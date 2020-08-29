
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import create_app
from api.model.model import setup_db, db, Category, Book

ADMIN_TOKEN = os.environ.get('ADMIN_TOKEN')
USER_TOKEN = os.environ.get('USER_TOKEN')


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # create app - api.py
        self.app = create_app()
        self.client = self.app.test_client
        # create db - model.py & binds the app to the current context
        with self.app.app_context():
            self.database_path = "postgresql://{}:{}@{}/{}".format(
                'admin', 'admin', 'localhost:5432', "library_test")
            setup_db(self.app, self.database_path)
            db.create_all()
            # add new test Category
            new_category = Category(name="Test Category")
            new_category.insert()

        # self.new_category = {
        #     "name": "Poems"
        # }
        # self.new_book = {
        #     "title": "Anansi Boys",
        #     "category": "Poems"
        # }
        #
        # self.admin_header = {
        #     "Authorization": f"Bearer {ADMIN_TOKEN}"
        # }
        #
        # self.user_header = {
        #     "Authorization": f"Bearer {USER_TOKEN}"
        # }

    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            categories = Category.query.all()
            for category in categories:
                category.delete()

    def test_202_post_books(self):
        # res = self.client().get('/books', json={'rating': 1}, headers=self.admin_header)
        # hello = "hello"
        self.assertEqual(hello, "hello")

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
