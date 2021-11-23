from flask_restful import Resource
from flask import jsonify, request
from model.movie_model import Movie
from model.genre_model import Genre
from utils.schemas import MovieSchema
from urls import db
from conf.auth import auth
from conf import role_required


class MovieHandler(Resource):
    @auth.login_required
    @role_required.permission(0)
    def get(self):
        args = request.args
        print(len(args))

        try:
            if 'name' in args:
                result = Movie.query.filter(Movie.name.like("%{0}%".format(args['name']))).join(Genre,
                                                                                                Movie.genres).all()
            else:
                result = Movie.query.join(Genre, Movie.genres).all()
            movies_schema = MovieSchema(many=True)
            # Get json data
            data = movies_schema.dump(result)
            return jsonify({'status': 'success', 'movies': data})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

    @auth.login_required
    @role_required.permission(1)
    def post(self):
        try:
            data = request.get_json()
            movie = Movie(popularity=str(data['99popularity']), director=data['director'],
                          imdb_score=str(data['imdb_score']),
                          name=data['name'])
            db.session.add(movie)

            for genre_item in data['genre']:
                exist_genre_item = Genre.query.filter(Genre.name == genre_item).first()
                if exist_genre_item is not None:
                    print('data is available')


                else:
                    print('')
                    exist_genre_item = Genre(name=genre_item)
                    db.session.add(exist_genre_item)
                movie.genres.append(exist_genre_item)

            db.session.commit()
            return jsonify({"status": "success", "message": "Data save successfully!"})
        except Exception as e:
            return jsonify({"status": "error", "message": "Data is not save successfully! Please try again"})
