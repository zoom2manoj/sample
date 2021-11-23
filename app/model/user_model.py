from flask_sqlalchemy import SQLAlchemy
from conf.auth import auth
from flask import g
import datetime
from config import Config
import jwt
from urls import db


class UserDetails(db.Model):
    # Generates default class name for table. For changing use
    # __tablename__ = 'userdetails'

    # UserDetails id.
    id = db.Column(db.Integer, primary_key=True)

    # UserDetails name.
    username = db.Column(db.String(length=80), unique=True, nullable=False)

    # UserDetails password.
    password = db.Column(db.String(length=80))

    # UserDetails email address.
    email = db.Column(db.String(length=80), unique=True, nullable=False)

    # Creation time for user.
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    # Unless otherwise stated default role is user.
    user_role = db.Column(db.String(length=80), default="user")

    # Generates auth token.
    def generate_auth_token(self, permission_level):
        # import pdb; pdb.set_trace()
        admin_value = 0
        # Check if admin.
        if permission_level == 1:
            admin_value = permission_level
        elif permission_level == 2:
            admin_value = permission_level
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=Config.JWT_TOKEN_EXPIRE),
            'iat': datetime.datetime.utcnow(),
            'sub': {"email": self.email, "admin": admin_value}
        }

        # Return normal user flag.
        # return jwt.dumps({"email": self.email, "admin": 0})

        return jwt.encode(
            payload,
            Config.SECRET_KEY,
            algorithm=Config.JWT_ALGORITHMS
        )

    # Generates a new access token from refresh token.
    @staticmethod
    @auth.verify_token
    def verify_auth_token(token):
        # import pdb; pdb.set_trace()
        # Create a global none user.
        g.user = None

        try:
            # Load token.
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=Config.JWT_ALGORITHMS)
        except:
            # If any error return false.
            return False

        # Check if email and admin permission variables are in jwt.
        if "email" and "admin" in data['sub']:
            # Set email from jwt.
            g.user = data['sub']["email"]

            # Set admin permission from jwt.
            g.admin = data['sub']["admin"]

            # Return true.
            return True

        # If does not verified, return false.
        return False

    @staticmethod
    def black_list_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            is_blacklisted_token = Blacklist.check_blacklist(auth_token)
            return is_blacklisted_token
        except Exception as e:
            return True

    def __repr__(self):

        # This is only for representation how you want to see user information after query.
        return "<UserDetails(id='%s', name='%s', password='%s', email='%s', created='%s')>" % (
            self.id,
            self.username,
            self.password,
            self.email,
            self.created,
        )


class Blacklist(db.Model):
    # Generates default class name for table. For changing use
    # __tablename__ = 'users'

    # Blacklist id.
    id = db.Column(db.Integer, primary_key=True)

    # Blacklist invalidated refresh tokens.
    refresh_token = db.Column(db.String(length=255))
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, refresh_token):
        self.refresh_token = refresh_token
        self.blacklisted_on = datetime.datetime.now()

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = Blacklist.query.filter_by(refresh_token=str(auth_token)).first()
        if res:
            return True
        else:
            return False

    def __repr__(self):
        # This is only for representation how you want to see refresh tokens after query.
        return "<UserDetails(id='%s', refresh_token='%s', status='invalidated.')>" % (
            self.id,
            self.refresh_token,
            self.blacklisted_on
        )
