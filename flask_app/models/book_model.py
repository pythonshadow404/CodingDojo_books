from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Book:
    DB = "books_schema"
    def __init__(self,data) -> None:
        self.id = data["id"]
        self.title = data["title"]
        self.author = data["author"]
        self.description = data["description"]
        self.pages = data["pages"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

    @classmethod
    def save(cls, data):
        query = "INSERT INTO books (title, author, description, pages, user_id) VALUES (%(title)s, %(author)s, %(description)s, %(pages)s, %(user_id)s)"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL(cls.DB).query_db(query)
        books = []
        for book in results:
            books.append(cls(book))
        return books
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM books WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])
    
    @classmethod
    def update_one(cls, data):
        # update the fields we actually want to edit
        query = "UPDATE books SET title = %(title)s,  author = %(author)s, description = %(description)s,\
            pages = %(pages)s WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM books WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)