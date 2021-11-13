# coding: utf-8

from app import db

class Author(db.Model):
    __tablename__ = "authors"
    author_id = db.Column("AuthorId", db.Integer, primary_key=True)
    name = db.Column("Name", db.Text(120))
    books = db.relationship("Book", backref="author")

class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column("BookId", db.Integer, primary_key=True)
    title = db.Column("Title", db.Text(160), nullable=False)
    author_id = db.Column(
        "AuthorId",
        db.ForeignKey("authors.author_id"),
        nullable=False,
        index=True,
    )
