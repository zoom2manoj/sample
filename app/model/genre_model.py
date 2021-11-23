"""Data models."""
from urls import db


# from sqlalchemy.orm import relationship


class Genre(db.Model):
    """Data model for genre."""

    __tablename__ = "genre"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Genre {}>".format(self.name)
