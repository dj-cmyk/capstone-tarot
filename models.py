"""SQLAlchemy models for Tarot App DB."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Test(db.Model):
    """docstring"""

    __tablename__ = 'tests'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )




def connect_db(app):
    """Connect this database to Flask app """

    db.app = app
    db.init_app(app)