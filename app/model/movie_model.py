"""Data models."""
from urls import db


movie_genre_c = db.Table(
    'movie_genre',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id')),
)


class Movie(db.Model):
    """Data model for movie"""
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True)
    popularity = db.Column(db.String(4), unique=False, nullable=False)
    director = db.Column(db.String(250), unique=False, nullable=False)
    imdb_score = db.Column(db.String(4), unique=False, nullable=False)
    name = db.Column(db.String(250), unique=False, nullable=False)
    genres = db.relationship("Genre", secondary=movie_genre_c, backref=db.backref('genreser', lazy='dynamic'))

    def __init__(self, popularity, director, imdb_score, name):
        self.popularity = popularity
        self.director = director
        self.imdb_score = imdb_score
        self.name = name

    def __repr__(self):
        return "<Movie {}>".format(self.name)
