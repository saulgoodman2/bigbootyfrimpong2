"""Initialize Flask app."""
from pathlib import Path

from flask import Flask, redirect, url_for, render_template, request, session, flash


# TODO: Access to the books should be implemented via the repository pattern and using blueprints, so this can not stay here!
from library.domain.model import Book

import library.adapters.jsondatareader as repo

# TODO: Access to the books should be implemented via the repository pattern and using blueprints, so this can not stay here!
def create_some_book():
    some_book = Book(1, "Harry Potter and the Chamber of Secrets")
    some_book.description = "Ever since Harry Potter had come home for the summer, the Dursleys had been so mean \
                             and hideous that all Harry wanted was to get back to the Hogwarts School for \
                             Witchcraft and Wizardry. But just as he’s packing his bags, Harry receives a \
                             warning from a strange impish creature who says that if Harry returns to Hogwarts, \
                             disaster will strike."
    some_book.release_year = 1999
    return some_book


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object('config.Config')
    data_path = Path('libray') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']



    @app.route('/')
    def home():
        some_book = create_some_book()
        # Use Jinja to customize a predefined html page rendering the layout for showing a single book.
        return render_template('home/home.html', book=some_book)

    # login page of website
    # post for safe delivery of information
    # session keeps user logged in, flash flashes a message when an action is done
    @app.route("/login", methods=["POST", "GET"])
    def login():
        if request.method == "POST":
            user = request.form["nm"]
            session["user"] = user
            flash("Login Successful!")
            return redirect(url_for("user"))
        else:
            if "user" in session:
                flash("Already Logged In!")
                return redirect(url_for("user"))

            return render_template("login.html")

    # shows login screen if user not logged in, otherwise shows user.html
    @app.route("/user")
    def user():
        if "user" in session:
            user = session["user"]
            return render_template("user.html", user=user)
        else:
            flash("You are not logged in!")
            return redirect(url_for("login"))

    # shows logout screen
    @app.route("/logout")
    def logout():
        flash("You have been logged out", "info")
        session.pop("user", None)
        return redirect(url_for("login"))

    @app.route("/world_of_books")
    def world_of_books():
        some_book = create_some_book()
        # Use Jinja to customize a predefined html page rendering the layout for showing a single book.
        return render_template('world_of_books.html', book=some_book)

    @app.route("/browse_by_title")
    def browse_by_title():
        some_book = create_some_book()
        # Use Jinja to customize a predefined html page rendering the layout for showing a single book.
        return render_template('browse_by_title.html', book=some_book)

    @app.route("/browse_by_author")
    def browse_by_author():
        some_book = create_some_book()
        # Use Jinja to customize a predefined html page rendering the layout for showing a single book.
        return render_template('browse_by_author.html', book=some_book)

    @app.route("/browse_by_year")
    def browse_by_year():
        some_book = create_some_book()
        # Use Jinja to customize a predefined html page rendering the layout for showing a single book.
        return render_template('browse_by_year.html', book=some_book)


    return app
