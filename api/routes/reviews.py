import json
from datetime import timedelta, date
from functools import wraps
from flask_jwt_extended import create_refresh_token, decode_token
from flask_restx.reqparse import HTTPStatus
from passlib.hash import sha256_crypt

from flask import request, jsonify
from flask_restx import Namespace, Resource
from flask_jwt_extended import create_access_token, get_jwt, jwt_required

from schemas.reviews import ProfileSchema
from core.redis import access_blocklist, refresh_blocklist
from core.db import reviews_data, users_data, bio_data
from bson import ObjectId
from json import dumps
from nanoid import generate



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
    # @validate_request(ProfileSchema)
    @jwt_required()
    def get(self):
        try:
            whole_token = get_jwt()
            user_id = whole_token["sub"]

            print(user_id)

            all_reviews = []
            user_reviews = reviews_data.find({"user_id": user_id})

            for review in user_reviews:
                new_review = {
                    "_id": review["_id"],
                    "movie_title": review["movie_title"],
                    "movie_description": review["movie_description"],
                    "movie_genres": review["movie_genres"],
                    "movie_url": review["movie_url"],
                    "review_date": review["review_date"],
                    "date_booked": review["review_date"],
                    "complete": review["complete"],
                }

                # new_review = {
                #     "_id": generate(),
                #     "user_id": user_id,
                #     "movie_title": movie_title,
                #     "movie_description": movie_description,
                #     "movie_genres": movie_genres,
                #     "movie_url": movie_url,
                #     "review_date": date_of_review,
                #     "date_booked": str(date.today()),
                #     "complete": False
                # }

                all_reviews.append(new_review)

            return {"message": "Reviews Found", "success": True, "data": all_reviews}, 200
        except:
            return {"message": "Failed to load reviews", "success": False, "data": []}, 500


@api.route("/view_biodata/<review_id>")
class Biodata(Resource):
    @jwt_required()
    def get(self, review_id):
        try:
            biodata = bio_data.find({"review_id": review_id})
            data_list = []

            for participant in biodata:
                data_set_list = []

                for heart_rate, sweat, timestamp in zip(participant["heart_rate"], participant["sweat"], participant["timestamp"]):
                    new_heart_rate = {
                        "group": "Heart Rate",
                        "timestamp": str(timedelta(seconds=timestamp)),
                        "value": heart_rate
                    }
                    new_sweat_rate = {
                        "group": "Perspiration",
                        "timestamp": str(timedelta(seconds=timestamp)),
                        "value": sweat
                    }

                    data_set_list.append(new_heart_rate)
                    data_set_list.append(new_sweat_rate)

                new_data_set = {
                    "machine_id": participant["machine_id"],
                    "data_set": data_set_list,
                    "average_sweat": participant["average_sweat"],
                    "average_heart_rate": participant["average_heart_rate"],
                }

                data_list.append(new_data_set)

            return {"message": "Review data found", "success": True, "data": data_list}
        except:
            return {"message": "Failed to load review data", "success": False, "data": []}


@api.route("/book")
class BookReview(Resource):
    @jwt_required()
    def post(self):
        try:
            movie_title = request.json["movie_title"]
            movie_description = request.json["movie_description"]
            movie_genres = request.json["movie_genres"]
            movie_url = request.json["movie_url"]
            date_of_review = request.json["review_date"]

            whole_token = get_jwt()
            user_id = whole_token["sub"]

            new_review = {
                "_id": generate(),
                "user_id": user_id,
                "movie_title": movie_title,
                "movie_description": movie_description,
                "movie_genres": movie_genres,
                "movie_url": movie_url,
                "review_date": date_of_review,
                "date_booked": str(date.today()),
                "complete": False
            }
            reviews_data.insert_one(new_review)

            return {"message": "Review booked successfully", "success": True, "data": new_review}
        except:
            return {"message": "Failed to book review", "success": False, "data": []}

