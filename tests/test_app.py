
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

    def add_book(self, category=None):
        with self.app.app_context():
            # add new demo data into postgres
            random_id = randint(1000000, 9999999)
            new_book = Book(name=f"Test_Book_{random_id}")
            if category is not None:
                new_book.category = category
            else:
                new_category = self.add_category()
                new_book.category = Category.query.filter(
                    Category.name == new_category.get('name')).first()
            new_book.insert()
            return {"id": new_book.id,
                    "name": new_book.name,
                    "category": new_book.category.name}

    def add_category(self):
        with self.app.app_context():
            # add new demo data into postgres
            random_id = randint(1000000, 9999999)
            new_category = Category(name=f"Test_Category_{random_id}")
            new_category.insert()
            return {"id": new_category.name,
                    "name": new_category.name}

    # GET /books - ADMIN_TOKE
    # success
    def test_200_get_books(self):
        new_book = self.add_book()
        header = self.self.admin_jw
        res = self.client().get('/books', headers=header)
        self.assertEqual(res.status_code, 200)

    # failure
    def test_422_get_books(self):
        self.delete_data()
        header = self.admin_jwt
        res = self.client().get('/books', headers=header)
        self.assertEqual(res.status_code, 422)

    # GET /categories - ADMIN_TOKE
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

    # POST /books - ADMIN_TOKE
    # success
    def test_200_post_books(self):
        random_id = randint(1000000, 9999999)
        new_book_name = "Test_Book_{random_id}"
        request_body = {"name": new_book_name,
                        "category": self.add_category().get("name")}
        header = self.admin_jwt
        res = self.client().post('/books', json=request_body, headers=header)
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(new_book_name, res_data.get("name"))

    def test_422_post_books(self):
        random_id = randint(1000000, 9999999)
        new_book_name = "Test_Book_{random_id}"
        request_body = {"name": new_book_name,
                        "category": "not_existed_category_name"}
        header = self.admin_jwt
        res = self.client().post('/books', json=request_body, headers=header)
        self.assertEqual(res.status_code, 422)

    # DELETE /books - ADMIN_TOKE
    # success
    def test_200_delete_books(self):
        new_book = self.add_book()
        request_body = {"name": new_book.get("name"),
                        "category": new_book.get("category")}
        header = self.admin_jwt
        res = self.client().delete('/books', json=request_body, headers=header)
        self.assertEqual(res.status_code, 200)

    def test_422_delete_books(self):
        random_id = randint(1000000, 9999999)
        new_book_name = "Test_Book_{random_id}"
        request_body = {"name": new_book_name,
                        "category": "not_existed_category_name"}
        header = self.admin_jwt
        res = self.client().delete('/books', json=request_body, headers=header)
        self.assertEqual(res.status_code, 422)

    # PATCH / books - ADMIN_TOKE
    # success

    def test_200_patch_books(self):
        new_book = self.add_book()
        new_book_id = new_book.get("id")
        new_category = self.add_category()
        new_category_name = new_category.get("name")
        request_body = {"category": new_category_name}
        header = self.admin_jwt
        res = self.client().patch(f'/books/{new_book_id}', json=request_body,
                                  headers=header)
        self.assertEqual(res.status_code, 200)

    # failure
    def test_422_patch_books(self):
        new_book = self.add_book()
        new_book_id = new_book.get("id")
        new_category = self.add_category()
        new_category_name = new_category.get("name")
        request_body = {"category": "not_exiting_category"}
        header = self.admin_jwt
        res = self.client().patch(f'/books/{new_book_id}', json=request_body,
                                  headers=header)
        self.assertEqual(res.status_code, 400)

    # RBAC for USER_TOKEN
    def test_200_USER_TOKEN(self):
        new_book = self.add_book()
        header = self.user_jwt
        res = self.client().get('/books', headers=header)
        self.assertEqual(res.status_code, 200)

    def test_422_USER_TOKEN(self):
        random_id = randint(1000000, 9999999)
        new_book_name = "Test_Book_{random_id}"
        request_body = {"name": new_book_name,
                        "category": self.add_category().get("name")}
        header = self.user_jwt
        res = self.client().post('/books', json=request_body, headers=header)
        self.assertEqual(res.status_code, 403)


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite)
    # unittest.main()
