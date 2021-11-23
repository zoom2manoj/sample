"""Application routes."""

from flask import current_app as app
from flask_restful import Api
from handler.movie_handler import MovieHandler
from handler.user_handler import Logout, RefreshToken, Register, ResetPassword, UsersData, DataSuperAdminRequired, \
    Login, DataAdminRequired, DataUserRequired
from datetime import datetime


@app.route('/')
def index():
    now = datetime.now()
    return str(now.strftime("%d/%m/%Y %H:%M:%S"))


# Create api.
api = Api(app)
api.add_resource(MovieHandler, "/v1/api/movie")

# Register page.
api.add_resource(Register, "/v1/auth/register")

# Login page.
api.add_resource(Login, "/v1/auth/login")

api.add_resource(Logout, "/v1/auth/logout")
# Refresh page.
api.add_resource(RefreshToken, "/v1/auth/refresh")

# Password reset page. Not forgot.
api.add_resource(ResetPassword, "/v1/auth/password_reset")

# Example user handler for user permission.
api.add_resource(DataUserRequired, "/data_user")

# Example admin handler for admin permission.
api.add_resource(DataAdminRequired, "/data_admin")

# Example user handler for user permission.
api.add_resource(DataSuperAdminRequired, "/data_super_admin")

# Get users page with admin permissions.
api.add_resource(UsersData, "/users")



