# Library
## Content
1.  Motivation
2.  Installing Dependencies
3.  Running server locally
4.  Endpoints
5.  Authentication
6.  Testing
7.  Running server on Heroku

## Motivation
This project covers the following technical topics:

-   Database modeling with postgres & sqlalchemy
-   API to performance CRUD Operations on database with Flask
-   Automated testing with Unittest
-   Authorization & Role based Authentification with Auth0
-   Deployment on Heroku

It resembles a library API which is responsible for creating books, categories and assigning a book to specific existing category. Within the library there are two roles: admin and user.

## Installing Dependencies
#### Python 3.7

Follow instructions to install the latest version of python for your platform in the  [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### [](https://github.com/khaled197/Udacity-FSND-Capstone-Casting-Agency#virtual-enviornment)Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the  [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### [](https://github.com/khaled197/Udacity-FSND-Capstone-Casting-Agency#pip-dependencies)PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

pip install -r requirements.txt

This will install all of the required packages we selected within the  `requirements.txt`  file.

##### [](https://github.com/khaled197/Udacity-FSND-Capstone-Casting-Agency#key-dependencies)Key Dependencies

-   [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.
-   [SQLAlchemy](https://www.sqlalchemy.org/)  and  [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)  are libraries to handle the postgresql database.
-   [jose](https://python-jose.readthedocs.io/en/latest/)  JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## [](https://github.com/khaled197/Udacity-FSND-Capstone-Casting-Agency#running-server-locally)Running server locally

Each time you open a new terminal session, run:

    source setup.sh
    export FLASK_APP=api.py;

To run the server, execute:

    flask run --reload

The  `--reload`  flag will detect file changes and restart the server automatically.
## Endpoints

```
GET /books
GET /categories
POST /books
POST /categories
DELETE /books
PATCH /books/<int:book_id>
```

#### GET /books
- Fetches a list of books
- Request Arguments: None
- Returns: An object with a success key and a list of books.

***response***
```
    {
	    "books": [
					{"category_id": 3,"id": 3,"name": "C++ principles"},
					{"category_id": 3, "id": 2,"name": "Python Programming"}
				 ],

	    "success": true
	    "total_books": 2

    }

```

#### GET /categories
- Fetches a list of categories
- Request Arguments: None
- Returns: An object with a success key and a list of categories.

***response***
```
{
	"categories": [
					{ "id": 2, "name": "History"},
					{ "id": 1, "name": "Poems"},
					{"id": 3, "name": "Programming"}
				  ],
	"success": true,
	"total_categories": 3
}
```
#### POST /books
- Post a new book
- Request Arguments: None
- Returns: An object with a success key and book attributes

***body***
```
{
"name" : "C++ principles",
"category" : "Programming"
}
```

***response***
```
{
"id": 3,
"name": "C++ principles",
"success": true
}
```


### POST /categories
- Post a new category
- Request Arguments: None
- Returns: An object with a success key and category attributes

***body***
```
{
	"name" : "Programming"
}
```
***response***
```
{
	"id": 3,
	"name": "Programming",
	"success": true
}
```

### DELETE /book/
- Delete an existing book
- Request Arguments: None
- Returns: An object with a success key and deleted book attributes

***body***
```
{
	"name" : "C++ principles"
}
```
***response***
```
{
"book_name_deleted": "C++ principles",
"success": true
}
```

### PATCH /books/book_id
- Update an existing book and change its category
- Request Arguments: book id
- Returns: An object with a success key and updated book attributes

***body***
```
{
	"category" : "Programming"
}
```

***response***
```
{
	"book_id_updated": 2,
	"success": true
}
```

## Authentication



#### Setup Auth0

 -  Create a new Auth0 Account
 -  Select a unique tenant domain
 -  Create a new, regular web application
 -  Create a new API
    -   in API Settings:
        -   Enable RBAC
        -   Enable Add Permissions in the Access Token
 -  Create new API permissions:
```
 - get:books
 - post:books
 - post:categories
 - get:categories
 - delete:books
 - patch:books
```
 -   Create new roles for:
	 -  admin: library admin can do all tasks.
	 - user: library user can do only read only books & categories.

## Testing

To run the tests, run

```
$ . setup.sh
$ python -m unittest -v
```

## Running server on Heroku

The application runs:

[library on heroku](https://fsnd-capstone-library.herokuapp.com/)
