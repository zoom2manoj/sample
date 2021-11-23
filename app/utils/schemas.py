from marshmallow import Schema, fields


class MovieGenreSchema(Schema):
    id = fields.Int()
    genre_id = fields.Nested('MovieSchema', many=False)
    movie_id = fields.Nested('GenreSchema', many=False)


class GenreName(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ''
        return value.name


class GenreSchema(Schema):
    """
    UserDetails schema returns only username, email and user role. This was used in user handlers.
    """

    name = fields.Str()


class MovieSchema(Schema):
    """
    Movies schema returns only popularity, director, imdb_score and name. This was used in movie handlers.
    """

    # Schema parameters.
    popularity = fields.Str()
    director = fields.Str()
    imdb_score = fields.Str()
    name = fields.Str()
    genres = fields.List(GenreName(), many=True)


class BaseUserSchema(Schema):
    """
    Base user schema returns all fields but this was not used in user handlers.
    """

    # Schema parameters.

    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Str()
    password = fields.Str()
    created = fields.Str()


class UserSchema(Schema):
    """
    UserDetails schema returns only username, email and creation time. This was used in user handlers.
    """

    # Schema parameters.

    username = fields.Str()
    email = fields.Str()
    created = fields.Str()
