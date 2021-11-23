"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from utils.util import read_data


db = SQLAlchemy()


def initial_db():
    from model.movie_model import Movie
    from model.genre_model import Genre
    try:
        data = read_data()
        for item in data:
            movie_exist = Movie.query.filter_by(popularity=str(item['99popularity']), director=item['director'],
                                                imdb_score=str(item['imdb_score']),
                                                name=item['name']).first()
            if movie_exist is not None:
                movie = movie_exist
            else:
                movie = Movie(popularity=str(item['99popularity']), director=item['director'],
                              imdb_score=str(item['imdb_score']),
                              name=item['name'])
                db.session.add(movie)
            for genre_item in item['genre']:
                genre_item = genre_item.strip()
                genre_data = Genre(genre_item)
                try:
                    exists = Genre.query.filter_by(name=genre_item).first()
                    if exists is not None:
                        genre_data = exists
                    else:
                        db.session.add(genre_data)
                except Exception as e:
                    print(str(e))
                    # pass
                movie.genres.append(genre_data)
                print('**')
            db.session.commit()
        print('in initial db')
    except Exception as e:
        print('error')
        print(str(e))


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")
    # Initialize Flask-BabelEx
    # babel = Babel(app)

    db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes
        from conf.db_initializer import create_admin_user, create_super_admin, create_test_user

        db.create_all()  # Create database tables for our data models
        # Create default super admin user in database.
        create_super_admin()

        # Create default admin user in database.
        create_admin_user()

        # Create default test user in database.
        create_test_user()

        try:
            initial_db()
        except Exception as e:
            pass

        return app
