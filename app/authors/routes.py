from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired
from wtforms.validators import ValidationError
from app import db
from app.models import Author, Book


# Setup the Blueprint
authors_bp = Blueprint(
    "authors_bp", __name__, template_folder="templates", static_folder="static"
)


def does_author_exist(form, field):
    author = (
        db.session.query(Author)
        .filter(Author.name == field.data)
        .one_or_none()
    )
    if author is not None:
        raise ValidationError("Author already exists", field.data)


class CreateAuthorForm(FlaskForm):
    name = StringField(
        label="Author's Name", validators=[InputRequired(), does_author_exist]
    )


@authors_bp.route("/")
@authors_bp.route("/authors", methods=["GET", "POST"])
def authors():
    form = CreateAuthorForm()

    # Is the form valid?
    if form.validate_on_submit():
        # Create new author
        author = Author(name=form.name.data)
        db.session.add(author)
        db.session.commit()
        return redirect(url_for("authors_bp.authors"))

    authors = db.session.query(Author).order_by(Author.name).all()
    return render_template("authors.html", authors=authors, form=form)