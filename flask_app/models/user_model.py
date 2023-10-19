from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.book_model import Book
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    DB = "books_schema"
    def __init__(self, data):
        # three (3) of the column are automatically generated and we have to supply 
        # the other three (username, email, password).
        # whenever we create a model we do include all our database columns
        self.id = data["id"] # self dot "whatever" equals data of "whatever"
        self.username = data["username"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.books = []

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (username, email, password)\
            VALUES (%(username)s, %(email)s, %(password)s)"
        return connectToMySQL(cls.DB).query_db(query,data)
        
    @classmethod
    # In order to login we need to look up the email
    # to see if it already exists.
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])
        
    @classmethod
    # Once we are logged in, we want to be able to look up the id of
    # of the logged-in user which we stored and returns 
    # all of the user's books.
    def get_by_id(cls,data):
        query = "SELECT * FROM users LEFT JOIN books ON users.id = books.user_id WHERE users.id = %(id)s"
        results = connectToMySQL(cls.DB).query_db(query,data)
        # Any query that we're selecting from always returns a list rather than a dictionary
        # we just want the first item in the list which would be the user the first book in their
        # database
        print(results)
        user = cls(results[0])
        for row in results:
            book_data = {
                "id":row["books.id"],
                "title":row["title"],
                "author":row["author"],
                "description":row["description"],
                "pages":row["pages"],
                "created_at":row["created_at"],
                "updated_at":row["updated_at"],
                "user_id":row["id"],
            }
            # a user object that has a list of a bunch of book objects
            user.books.append(Book(book_data))
        return user
        
    @staticmethod
    # we are grabbing request.form data
    def validate_user(user):
        is_valid = True
        if len(user["username"]) < 5 or len(user["username"]) > 20:
            flash("Username must be between 5 and 20 characters!")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]):
            flash("Invalid Email")
        if len(user["password"]) < 5 or len(user["password"]) > 20:
            flash("Password must be between 5 and 20 characters!")
            is_valid = False
        return is_valid
