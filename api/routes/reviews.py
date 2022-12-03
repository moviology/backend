import json
from datetime import timedelta
from functools import wraps
from flask_jwt_extended import create_refresh_token, decode_token
from flask_restx.reqparse import HTTPStatus
from passlib.hash import sha256_crypt

from flask import request, jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from schemas.reviews import ProfileSchema
from core.redis import access_blocklist, refresh_blocklist
from core.db import reviews_data, users_data
from bson import ObjectId
from json import dumps



########################
# Initialize namespace #
########################
api = Namespace("reviews", description="Management of user reviews and related biometric data")


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


@api.route("/profile")
class Profile(Resource):
    @validate_request(ProfileSchema)
    @jwt_required()
    def get(self):
        try:
            whole_token = get_jwt()
            user_id = whole_token["sub"]

            all_reviews = []
            user_reviews = reviews_data.find({"user_id": user_id})

            for review in user_reviews:
                new_review = {
                    "_id": review["_id"],
                    "movie_title": review["movie_title"],
                    "movie_description": review["movie_description"],
                    "movie_genres": review["movie_genres"],
                    "review_date": review["review_date"],
                    "complete": review["complete"],
                }

                all_reviews.append(new_review)

            return {"message": "Reviews Found", "success": True, "data": all_reviews}, 200
        except:
            return {"message": "Failed to load reviews", "success": False, "data": []}, 500
