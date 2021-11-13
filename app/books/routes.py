from flask import Blueprint, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import HiddenField
from wtforms.validators import InputRequired, ValidationError
from app import db
from app.models import Author, Book


# Setup the Blueprint
books_bp = Blueprint(
    "books_bp", __name__, template_folder="templates", static_folder="static"
)


def does_book_exist(form, field):
    book = (
        db.session.query(Book)
        .join(Author)
        .filter(Author.name == form.author.data)
        .filter(Book.title == field.data)
        .one_or_none()
    )

    if book is not None:
        raise ValidationError("Book already exists", field.data)


class CreateBookForm(FlaskForm):
    author = HiddenField("author")
    title = StringField(
        label="Book's Name", validators=[InputRequired(), does_book_exist]
    )


@books_bp.route("/books", methods=["GET", "POST"])
@books_bp.route("/books/<int:author_id>", methods=["GET", "POST"])
def books(author_id=None):
    form = CreateBookForm()

    # did we get an artist id?
    if author_id is not None:
        # Get the artist
        author = (
            db.session.query(Author)
            .filter(Author.author_id == author_id)
            .one_or_none()
        )
        form.author.data = author.name
    # otherwise, no artist
    else:
        author = None

    # Is the form valid?
    if form.validate_on_submit():
        # Create new Album
        book = Book(title=form.title.data)
        author.books.append(book)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for("books_bp.nooks", author_id=author_id))

    # Start the query for albums
    query = db.session.query(Book)

    # Display the albums for the artist passed?
    if author_id is not None:
        query = query.filter(Book.author_id == author_id)

    books = query.order_by(Book.title).all()

    return render_template(
        "books.html", author=author, books=books, form=form
    )
