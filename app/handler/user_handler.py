from flask_restful import Resource
import logging
import datetime
from flask import g, request
import conf.errors as error
from conf.auth import auth
import jwt
from urls import  db
from model.user_model import  Blacklist, UserDetails
from config import Config
from conf import role_required
from utils.schemas import UserSchema


class Register(Resource):
    @staticmethod
    def post():

        try:
            # Get username, password and email.
            username, password, email = (
                request.json.get("username").strip(),
                request.json.get("password").strip(),
                request.json.get("email").strip(),
            )
        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Username, password or email is wrong. " + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        # Check if any field is none.
        if username is None or password is None or email is None:
            return error.INVALID_INPUT_422

        # Get user if it is existed.
        user = UserDetails.query.filter_by(email=email).first()

        # Check if user is existed.
        if user is not None:
            return error.ALREADY_EXIST

        # Create a new user.
        user = UserDetails(username=username, password=password, email=email)

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        # Return success if registration is completed.
        return {"status": "registration completed."}


class Login(Resource):

    def post(self):

        try:
            # Get user email and password.
            email, password = (
                request.json.get("email").strip(),
                request.json.get("password").strip(),
            )

        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Email or password is wrong. " + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        # Check if user information is none.
        if email is None or password is None:
            return error.INVALID_INPUT_422

        # Get user if it is existed.
        user = UserDetails.query.filter_by(email=email, password=password).first()
        admin_value = 0
        # Check if user is not existed.
        if user is None:
            return error.UNAUTHORIZED

        if user.user_role == Config.USER_ROLE_NORMAL:

            # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
            access_token = user.generate_auth_token(0)
            admin_value = 0

        # If user is admin.
        elif user.user_role == Config.USER_ROLE_ADMIN:

            # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
            access_token = user.generate_auth_token(1)
            admin_value = 1

        # If user is super admin.
        elif user.user_role == Config.USER_ROLE_SUPER_ADMIN:

            # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 2, 1, 0.
            access_token = user.generate_auth_token(2)
            admin_value = 2

        else:
            return error.INVALID_INPUT_422

        # Generate refresh token.
        # refresh_token = refresh_jwt.dumps({"email": email})
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=Config.JWT_TOKEN_EXPIRE*6),
            'iat': datetime.datetime.utcnow(),
            'sub': {"email": email, "admin": admin_value}
        }

        refresh_token = jwt.encode(
            payload,
            Config.SECRET_KEY,
            algorithm=Config.JWT_ALGORITHMS
        )

        # Return access token and refresh token.
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }


class Logout(Resource):
    @auth.login_required
    def get(self):
        # import pdb; pdb.set_trace()
        # Get refresh token.
        # refresh_token = request.json.get("refresh_token")
        access_token = request.headers.get('Authorization').split(' ')[1]

        # Get if the refresh token is in blacklist
        ref = Blacklist.query.filter_by(refresh_token=access_token).first()

        # Check refresh token is existed.
        if ref is not None:
            return {"status": "already invalidated", "access_token": access_token}

        # delete unused data
        limit = datetime.datetime.now() - datetime.timedelta(seconds=Config.JWT_TOKEN_EXPIRE)
        Blacklist.query.filter(Blacklist.blacklisted_on < limit).delete()

        # Create a blacklist refresh token.
        blacklist_access_token = Blacklist(refresh_token=access_token)

        # Add refresh token to session.
        db.session.add(blacklist_access_token)

        # Commit session.
        db.session.commit()

        # Return status of refresh token.
        return {"status": "invalidated", "access_token": access_token}


class RefreshToken(Resource):
    @staticmethod
    @auth.login_required
    def post():
        # import pdb; pdb.set_trace()
        # Get refresh token.
        refresh_token = request.json.get("refresh_token")

        # Get if the refresh token is in blacklist.
        if UserDetails.black_list_auth_token(request.headers.get('Authorization').split(' ')[1]):
            return error.UNAUTHORIZED

        try:
            # Generate new token.
            data = jwt.decode(refresh_token, Config.SECRET_KEY, algorithms=Config.JWT_ALGORITHMS)

        except Exception as why:
            # Log the error.
            logging.error(why)

            # If it does not generated return false.
            return False

        role_value = 'user'
        if data['sub']['admin'] == 2:
            role_value = 'sa'
        elif data['sub']['admin'] ==1:
            role_value = 'admin'
        # Create user not to add db. For generating token.
        user = UserDetails(email=data['sub']["email"], user_role=role_value)

        # New token generate.
        token = user.generate_auth_token(data['sub']['admin'])
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=Config.JWT_TOKEN_EXPIRE*6),
            'iat': datetime.datetime.utcnow(),
            'sub': {"email": data['sub']["email"], "admin": data['sub']['admin']}
        }

        refresh_token = jwt.encode(
            payload,
            Config.SECRET_KEY,
            algorithm=Config.JWT_ALGORITHMS
        )

        # refresh_token = refresh_jwt.dumps({"email": data["email"]})
        # Return new access token.
        return {
            "access_token": token,
            "refresh_token": refresh_token,
        }


class ResetPassword(Resource):
    @auth.login_required
    def post(self):
        if UserDetails.black_list_auth_token(request.headers.get('Authorization').split(' ')[1]):
            return error.UNAUTHORIZED
        # Get old and new passwords.
        old_pass, new_pass = request.json.get("old_pass"), request.json.get("new_pass")

        # Get user. g.user generates email address cause we put email address to g.user in models.py.
        user = UserDetails.query.filter_by(email=g.user).first()

        # Check if user password does not match with old password.
        if user.password != old_pass:
            # Return does not match status.
            return {"status": "old password does not match."}

        # Update password.
        user.password = new_pass

        # Commit session.
        db.session.commit()

        # Return success status.
        return {"status": "password changed."}


class UsersData(Resource):
    @auth.login_required
    @role_required.permission(2)
    def get(self):
        try:
            if UserDetails.black_list_auth_token(request.headers.get('Authorization').split(' ')[1]):
                return error.UNAUTHORIZED
            # Get usernames.
            usernames = (
                []
                if request.args.get("usernames") is None
                else request.args.get("usernames").split(",")
            )

            # Get emails.
            emails = (
                []
                if request.args.get("emails") is None
                else request.args.get("emails").split(",")
            )

            # Get start date.
            start_date = datetime.datetime.strptime(request.args.get("start_date"), "%d.%m.%Y")

            # Get end date.
            end_date = datetime.datetime.strptime(request.args.get("end_date"), "%d.%m.%Y")

            print(usernames, emails, start_date, end_date)

            # Filter users by usernames, emails and range of date.
            users = (
                UserDetails.query.filter(UserDetails.username.in_(usernames))
                    .filter(UserDetails.email.in_(emails))
                    .filter(UserDetails.created.between(start_date, end_date))
                    .all()
            )

            # Create user schema for serializing.
            user_schema = UserSchema(many=True)

            # Get json data
            data, errors = user_schema.dump(users)

            # Return json data from db.
            return data

        except Exception as why:

            # Log the error.
            logging.error(why)

            # Return error.
            return error.INVALID_INPUT_422


# auth.login_required: Auth is necessary for this handler.
# role_required.permission: Role required user=0, admin=1 and super admin=2.


class DataUserRequired(Resource):
    @auth.login_required
    def get(self):
        if UserDetails.black_list_auth_token(request.headers.get('Authorization').split(' ')[1]):
            return error.UNAUTHORIZED
        return "Test user data."


class DataAdminRequired(Resource):
    @auth.login_required
    @role_required.permission(1)
    def get(self):
        if UserDetails.black_list_auth_token(request.headers.get('Authorization').split(' ')[1]):
            return error.UNAUTHORIZED
        return "Test admin data."


class DataSuperAdminRequired(Resource):
    @auth.login_required
    @role_required.permission(2)
    def get(self):
        if UserDetails.black_list_auth_token(request.headers.get('Authorization').split(' ')[1]):
            return error.UNAUTHORIZED
        return "Test super admin data."
