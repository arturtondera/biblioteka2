from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Define the application
app = Flask(__name__, instance_relative_config=False)

# Configure the application
app.config.from_object(Config)

# Define the database object
db = SQLAlchemy(app)

# Initialize Bootstrap connection
Bootstrap(app)

# Register Blueprings
from .authors import routes as author_routes  # noqa: E402
from .books import routes as book_routes  # noqa: E402

app.register_blueprint(author_routes.authors_bp)
app.register_blueprint(book_routes.books_bp)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


from app import models  # noqa: F401, E402