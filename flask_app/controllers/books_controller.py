from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user_model import User
from flask_app.models.book_model import Book

@app.route("/create/book", methods = ["POST"])
def create_book():
    Book.save(request.form)
    return redirect('/dashboard')

@app.route("/book/<int:id>")
def book(id):
    # get one book by its id
    data = {
        "id":id
    }
    book = Book.get_by_id(data)
    return render_template("book.html", book = book)

@app.route("/delete/book/<int:id>")
def delete_book(id):
    data = {
        "id":id
    }
    Book.delete_one(data)
    return redirect("/dashboard")

@app.route("/edit/book/<int:id>")
def edit_book(id):
    data = {
        "id":id
    }
    book = Book.get_by_id(data)
    return render_template("book_edit.html", book = book)

@app.route("/edit/book", methods = ["POST"])
def edit_one_book():
    Book.update_one(request.form)
    return redirect(f"/book/{request.form['id']}")

# Display/feed every book in our database to the template
@app.route("/feed")
def book_feed():
    books = Book.get_all()
    return render_template("all_books.html", books = books)
