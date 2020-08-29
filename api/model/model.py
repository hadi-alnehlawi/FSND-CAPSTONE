from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

db = SQLAlchemy()
database_name = "library"
user_name = "admin"
user_password = "admin"
host_name = "localhost"
database_port = 5432
database_path = f'postgresql://{user_name}:{user_password}@{host_name}:{database_port}/{database_name}'

def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['DEBUG'] = True
    db.init_app(app)
    migrate = Migrate(app, db)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {"id": self.id, "name": self.name, "category_id": self.category_id}

    def __repr__(self):
        return f"<id: {self.id} , name: {self.name}, category_id: {self.category_id}>"


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    books = db.relationship('Book', backref='category')

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {"id": self.id, "name": self.name}

    def __repr__(self):
        return f"<id: {self.id} , name: {self.name}>"
