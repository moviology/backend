from datetime import timedelta
from functools import wraps
from flask_jwt_extended import create_refresh_token, decode_token
from flask_restx.reqparse import HTTPStatus
from passlib.hash import sha256_crypt

from flask import request
from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from schemas.auth import LoginSchema, LogoutSchema, RefreshSchema, RegisterSchema
from core.redis import access_blocklist, refresh_blocklist
from core.db import users_data, reviews_data
from nanoid import generate

########################
# Initialize namespace #
########################
api = Namespace("auth", description="User authentication and session management")


################################
# Request Validation Decorator #
################################
def validate_request(Schema):
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            schema = Schema()
            error = schema.validate(data=request.get_json())
            if error:
                return {'message': 'Invalid Credentials', 'success': False, 'data': error}, 401
            else:
                return fn(*args, **kwargs)
        return wrapped
    return decorator


###############
# Auth Routes #
###############
@api.route("/register")
class Register(Resource):
    @validate_request(RegisterSchema)
    def post(self):
        user_name = request.json["name"]
        user_email = request.json["email"]
        user_pw = request.json["password"]

        if users_data.find_one({"email": user_email}) is not None:
            return {"message": "User already exists", "success": False, "data": {}}, 401

        encrypted_password = sha256_crypt.hash(user_pw)
        new_user = {
            "_id": generate(),
            "name": user_name,
            "email": user_email,
            "password": encrypted_password,
        }

        inserted_user = users_data.insert_one(new_user)
        access_token = create_access_token(identity=str(inserted_user.inserted_id), expires_delta=timedelta(minutes=5))
        refresh_token = create_refresh_token(identity=str(inserted_user.inserted_id), expires_delta=timedelta(weeks=2))

        return {
            "message": "Registration Successful",
            "success": True,
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "name": new_user["name"]
            },
        }, 200


@api.route("/login")
class LoginHandler(Resource):
    @validate_request(LoginSchema)
    def post(self):
        """
        Check if the user exists in database.
        Check if password hash matches.
        The respond back with user's username, refresh and access tokens
        """
        user_email = request.json["email"]
        user_pw = request.json["password"]
        fetched_user = users_data.find_one({"email": user_email})

        print(user_email)

        if fetched_user is None:
            return {'message': 'User not found', 'success': False, 'data': {}}, 401

        pw_verified = sha256_crypt.verify(user_pw, fetched_user["password"])

        if not pw_verified:
            return {
                "message": "Incorrect login details",
                "success": False,
                "data": {},
            }, 403

        access_token = create_access_token(identity=str(fetched_user["_id"]), expires_delta=timedelta(hours=2))
        refresh_token = create_refresh_token(identity=str(fetched_user["_id"]), expires_delta=timedelta(weeks=1))

        return {
            "message": "Login successful",
            "success": True,
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "name": fetched_user["name"]
            }
        }, 200


@api.route("/logout")
class LogoutHandler(Resource):
    @validate_request(LogoutSchema)
    @jwt_required()
    def post(self):
        """
        Decode the JWT access token in the request header and the refresh token
        in the request body and add them to the blocklist
        """
        # decode tokens
        access_token_jti = get_jwt()["jti"]
        refresh_token_jti = decode_token(request.json["refresh_token"])["jti"]

        print(request.json["refresh_token"])

        # add to blocklist
        access_blocklist.set(access_token_jti, "", ex=timedelta(hours=2))
        refresh_blocklist.set(refresh_token_jti, "", ex=timedelta(weeks=1))
        return {"message": "Logout successful", "success": True, "data": {}}, 200


@api.route("/refresh")
class RefreshHandler(Resource):
    @validate_request(RefreshSchema)
    @jwt_required(refresh=True)
    def get(self):
        """
        Decode the JWT refresh token in the request header and the access token
        in the request body and add them to the blocklist.
        Then generate a new a pair of refresh and access token and send back.
        """
        # decode tokens
        refresh_token = get_jwt()
        access_token = decode_token(request.json["access_token"])

        print(refresh_token["sub"])
        print(access_token["sub"])

        if refresh_token["sub"] != access_token["sub"]:
            return {
                "message": "Tokens were not issued by same user",
                "success": False,
                "data": {}
            }, HTTPStatus.UNAUTHORIZED

        # add to blocklist
        access_blocklist.set(access_token["jti"], "", ex=timedelta(hours=2))
        refresh_blocklist.set(refresh_token["jti"], "", ex=timedelta(weeks=1))

        # generate new tokens
        new_access_token = create_access_token(identity=str(access_token["sub"]), expires_delta=timedelta(hours=2))
        new_refresh_token = create_refresh_token(identity=str(access_token["sub"]), expires_delta=timedelta(weeks=1))

        return {
            "message": "Refresh successful",
            "success": True,
            "data": {
                "access_token": new_access_token,
                "refresh_token": new_refresh_token,
            }
        }, HTTPStatus.OK
