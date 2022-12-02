import json
import certifi
from pymongo import MongoClient
from urllib.parse import quote_plus
from main import config


uri = "mongodb+srv://%s:%s@%s.asjwyhf.mongodb.net/?retryWrites=true&w=majority" % (
    quote_plus(config.get("MONGO_USER")),
    quote_plus(config.get("MONGO_PASSWORD")),
    quote_plus(config.get("MONGO_DBNAME")),
)

client = MongoClient(uri, tlsCAFile=certifi.where())
db = client.Moviology

# CREATING COLLECTIONS ON THE DATABASE USING DB VARIABLE
bio_data = db.DATASETS
movies_data = db.MOVIES
reviews_data = db.REVIEWS
users_data = db.USERS


def all_datasets_data():
    try:
        data = bio_data.find()
        return data
    except Exception as e:
        raise e


def all_movies_data():
    try:
        data = movies_data.find()
        return data
    except Exception as e:
        raise e


def all_users_data():
    try:
        data = users_data.find()
        return data
    except Exception as e:
        raise e


def insert_one_into_dataset_collection(test_data):
    try:
        data = bio_data.insert_one(test_data)
        return data
    except Exception as e:
        raise e


def insert_one_into_user_collection(test_data):
    try:
        data = users_data.insert_one(test_data)
        return data
    except Exception as e:
        raise e


def insert_one_into_movie_collection(test_data):
    try:
        data = movies_data.insert_one(test_data)
        return data
    except Exception as e:
        return e


def insert_one_into_review_collection(test_data):
    try:
        data = reviews_data.insert_one(test_data)
        return data
    except Exception as e:
        raise e


def find_many_documents_in_dataset_with_common_variable(data_variable):
    try:
        data = bio_data.find(data_variable)
        return data
    except Exception as e:
        raise e


def find_many_documents_in_user_with_common_variable(data_variable):
    try:
        data = users_data.find(data_variable)
        return data
    except Exception as e:
        raise e


def find_many_documents_in_movie_with_common_variable(data_variable):
    try:
        data = movies_data.find(data_variable)
        return data
    except Exception as e:
        raise e


def find_many_documents_in_review_with_common_variable(data_variable):
    try:
        data = reviews_data.find(data_variable)
        return data
    except Exception as e:
        raise e


def find_user_by_id(user_id):
    try:
        data = users_data.find_one(user_id)
        return data
    except Exception as e:
        raise e


def find_movie_by_id(movie_id):
    try:
        data = movies_data.find_one(movie_id)
        return data
    except Exception as e:
        raise e


def find_dataset_by_id(dataset_id):
    try:
        data = bio_data.find_one(dataset_id)
        return data
    except Exception as e:
        raise e


def find_review_by_id(review_id):
    try:
        data = reviews_data.find_one(review_id)
        return data
    except Exception as e:
        raise e


def find_user_by_name(name):
    try:
        data = users_data.find_one(name)
        return data
    except Exception as e:
        raise e


def find_movie_by_name(name):
    try:
        data = movies_data.find_one(name)
        return data
    except Exception as e:
        raise e


def get_all_movie_genres():
    try:
        data = movies_data.distinct("genre")
        return data
    except Exception as e:
        raise e


def get_genres_for_movie_by_id(movie_id):
    try:
        data = movies_data.distinct("genre", {"movie_id": movie_id})
        return data
    except Exception as e:
        raise e


def get_genres_for_movie_by_name(movie_name):
    try:
        data = movies_data.distinct("genre", {"name": movie_name})
        return data
    except Exception as e:
        raise e


def get_max_timestamp_in_all_documents():
    try:
        data = bio_data.aggregate([
            {"$project":
                {"dataset_id": 1, "max_timestamp": {"$max": "$timestamp"}}
             }
        ])
        return data
    except Exception as e:
        raise e


def get_max_timestamp_by_dataset_id(dataset_id):
    try:
        data = bio_data.aggregate([
            {"$match": {"dataset_id": dataset_id}},
            {"$project":
                {"dataset_id": dataset_id, "max_timestamp": {"$max": "$timestamp"}}
             }
        ])
        data_list = list(data)
        data_index_0 = data_list[0]
        return data_index_0
    except Exception as e:
        raise e


def get_min_timestamp_in_all_documents():
    try:
        data = bio_data.aggregate([
            {"$project":
                {"dataset_id": 1, "min_timestamp": {"$min": "$timestamp"}}
             }
        ])
        return data
    except Exception as e:
        raise e


def get_min_timestamp_by_dataset_id(dataset_id):
    try:
        data = bio_data.aggregate([
            {"$match": {"dataset_id": dataset_id}},
            {"$project":
                {"dataset_id": dataset_id, "min_timestamp": {"$min": "$timestamp"}}
             }
        ])
        data_list = list(data)
        data_index_0 = data_list[0]
        return data_index_0
    except Exception as e:
        raise e


def get_max_heart_rate_in_all_documents():
    try:
        data = bio_data.aggregate([
            {"$project":
                {"dataset_id": 1, "max_heart_rate": {"$max": "$heart_rate"}}
             }
        ])
        return data
    except Exception as e:
        raise e


def get_max_heart_rate_by_dataset_id(dataset_id):
    try:
        data = bio_data.aggregate([
            {"$match": {"dataset_id": dataset_id}},
            {"$project":
                {"dataset_id": dataset_id, "max_heart_rate": {"$max": "$heart_rate"}}
             }
        ])
        data_list = list(data)
        data_index_0 = data_list[0]
        return data_index_0
    except Exception as e:
        raise e


def get_min_heart_rate_in_all_documents():
    try:
        data = bio_data.aggregate([
            {"$project":
                {"dataset_id": 1, "min_heart_rate": {"$min": "$heart_rate"}}
             }
        ])
        return data
    except Exception as e:
        raise e


def get_min_heart_rate_by_dataset_id(dataset_id):
    try:
        data = bio_data.aggregate([
            {"$match": {"dataset_id": dataset_id}},
            {"$project":
                {"dataset_id": dataset_id, "min_heart_rate": {"$min": "$heart_rate"}}
             }
        ])
        data_list = list(data)
        data_index_0 = data_list[0]
        return data_index_0
    except Exception as e:
        raise e


def get_max_sweat_in_all_documents():
    try:
        data = bio_data.aggregate([
            {"$project":
                {"dataset_id": 1, "max_sweat": {"$max": "$sweat"}}
             }
        ])
        return data
    except Exception as e:
        raise e


def get_max_sweat_by_dataset_id(dataset_id):
    try:
        data = bio_data.aggregate([
            {"$match": {"dataset_id": dataset_id}},
            {"$project":
                {"dataset_id": dataset_id, "max_sweat": {"$max": "$sweat"}}
             }
        ])
        data_list = list(data)
        data_index_0 = data_list[0]
        return data_index_0
    except Exception as e:
        raise e


def get_min_sweat_in_all_documents():
    try:
        data = bio_data.aggregate([
            {"$project":
                {"dataset_id": 1, "min_sweat": {"$min": "$sweat"}}
             }
        ])
        return data
    except Exception as e:
        raise e


def get_min_sweat_by_dataset_id(dataset_id):
    try:
        data = bio_data.aggregate([
            {"$match": {"dataset_id": dataset_id}},
            {"$project":
                {"dataset_id": dataset_id, "min_sweat": {"$min": "$sweat"}}
             }
        ])
        data_list = list(data)
        data_index_0 = data_list[0]
        return data_index_0
    except Exception as e:
        raise e


def get_max_user_id_in_collection():
    try:
        data = bio_data.aggregate([
            {"$group": {
                "_id": "$user_id",
                "max_user_id": {"$max": "$user_id"}
            }
            },
            {"$sort": {"_id": -1}},
            {"$limit": 1}
        ])
        return data
    except Exception as e:
        raise e


def get_min_user_id_in_collection():
    try:
        data = bio_data.aggregate([
            {"$group": {
                "_id": "$_id",
                "min_user_id": {"$min": "$user_id"}
            }
            },
            {"$sort": {"_id": 1}},
            {"$limit": 1}
        ])
        return data
    except Exception as e:
        raise e


def get_all_related_data_to_all_review_documents():
    try:
        data = reviews_data.aggregate([
            {"$lookup": {"from": 'DATASETS', "localField": 'dataset_id', "foreignField": "dataset_id", "as": "dataset_id"}},
            {"$lookup": {"from": 'MOVIES', "localField": 'movie_id', "foreignField": "movie_id", "as": "movie_id"}},
            {"$lookup": {"from": 'USERS', "localField": 'user_id', "foreignField": "user_id", "as": "user_id"}}
        ])
        return data
    except Exception as e:
        raise e


def get_all_related_data_to_reviews_by_review_id(review_id):
    try:
        data = reviews_data.aggregate([
            {"$match": {"review_id": review_id}},
            {"$lookup": {"from": 'DATASETS', "localField": 'dataset_id', "foreignField": "dataset_id", "as": "dataset_id"}},
            {"$lookup": {"from": 'MOVIES', "localField": 'movie_id', "foreignField": "movie_id", "as": "movie_id"}},
            {"$lookup": {"from": 'USERS', "localField": 'user_id', "foreignField": "user_id", "as": "user_id"}}
        ])
        data_list = list(data)
        data_index_0 = data_list[0]
        return data_index_0
    except Exception as e:
        raise e
