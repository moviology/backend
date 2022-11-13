from flask import Flask, redirect, render_template, request, session, url_for
from pymongo import MongoClient
from flask_session import Session
from urllib.parse import quote_plus
from bson.json_util import dumps
import json
import certifi
from passlib.hash import sha256_crypt

with open("../config/.secrets.json") as config_file:
    config = json.load(config_file)

app = Flask(__name__)
app.config["SECRET_KEY"] = config.get("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

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

# FETCHING ALL DATA FROM ALL 4 TABLES
all_bio_data = bio_data.find()
all_movies_data = movies_data.find()
all_reviews_data = reviews_data.find()
all_users_data = users_data.find()


# # CREATING TEST DATA
# testData = {
#     "dataset_id": 3,
#     "timestamp": [3, 6, 9, 12, 15],
#     "heart_rate": [100, 120, 109, 112],
#     "sweat": [0, 5, 6, 12],
#     "machine_id": 128219,
# }

# INSERTING TEST DATA INTO 'DATASETS' DATABASE
# bio_data.insert_one(testData)

# ITERATING THROUGH EACH ELEMENT IN all_bio_data
# for bioentry in all_bio_data:
#     #bioentry is dictionary
#     print(bioentry['machine_id'])
#     print(bioentry.items())

# PRINTING DATA FROM ALL TABLES IN JSON FORMAT
# print("Biometric data" + dumps(all_bio_data))
# print("Movie data" + dumps(all_movies_data))
# print("Review data" + dumps(all_reviews_data))
# print("User data" + dumps(all_users_data))
#
# print("\nFinding many entries that share common value for variable")
# for entry in bio_data.find({"machine_id": 128219}):  # finding many documents
#     print(entry)
#
# print("\nCounting entries")
# print(bio_data.count_documents({"machine_id": 128219}))
#
# # GETTING REVIEWS FOR A SINGLE MOVIE DIRECETOR USER
# testUser = users_data.find_one({"name": "kacper"})
# testUserId = testUser['user_id']
# print(f"\nUser name: {testUser['name']}")
# testReviews = reviews_data.find_one({"user_id": testUserId})
# print(f"\nReview description: {testReviews['description']}")
# testMovieId = testReviews['movie_id']
# testMovie = movies_data.find_one({"movie_id": testMovieId})
# print(f"\nMovie name: {testMovie['name']}")
# testDatasetId = testReviews['dataset_id']
# print(f"\nBiometric data")
# testBioData = bio_data.find({"dataset_id": testDatasetId})
#
# # ITERATING THROUGH ALL THE BIOMETRIC DATA THAT CORRESPOND TO THE SELECTED REVIEW, USING 'dataset_id' AS FOREIGN KEY
# for entry in testBioData:  # finding many documents
#     print(entry)
#
# GETS ALL REVIEWS DOCUMENTS ALONG WITH ALL THE APPROPRIATE DATASET, USERS, AND MOVIE DOCUMENTS
# aggregate_all_data_from_reviews_collection = reviews_data.aggregate([
#     {"$lookup": {"from": 'DATASETS', "localField": 'dataset_id', "foreignField": "dataset_id", "as": "dataset_id"}},
#     {"$lookup": {"from": 'MOVIES', "localField": 'movie_id', "foreignField": "movie_id", "as": "movie_id"}},
#     {"$lookup": {"from": 'USERS', "localField": 'user_id', "foreignField": "user_id", "as": "user_id"}}
# ])
#
# PRINTS OUT THE aggregate_all_data_from_reviews_collection DATA
# print("all data" + dumps(aggregate_all_data_from_reviews_collection))
#
#  GETS THE REVIEWS DOCUMENT BY REVIEW_ID ALONG WITH ALL THE APPROPRIATE DATASET, USERS, AND MOVIE DOCUMENTS
# aggregate_all_data_from_reviews_collection_by_id = reviews_data.aggregate([
#     {"$match": {"review_id": 282}},
#     {"$lookup": {"from": 'DATASETS', "localField": 'dataset_id', "foreignField": "dataset_id", "as": "dataset_id"}},
#     {"$lookup": {"from": 'MOVIES', "localField": 'movie_id', "foreignField": "movie_id", "as": "movie_id"}},
#     {"$lookup": {"from": 'USERS', "localField": 'user_id', "foreignField": "user_id", "as": "user_id"}}
# ])
#
# PRINTS OUT THE aggregate_all_data_from_reviews_collection_by_id DATA
# print("data by id" + dumps(aggregate_all_data_from_reviews_collection_by_id))
#
# // max timestamp in all DATASETS documents
# db.DATASETS.aggregate([
#     { "$project":
#         {"dataset_id": 1, "max_timestamp": { "$max": "$timestamp" }}
#     }
# ])
#
# // max timestamp by dataset id
# db.DATASETS.aggregate([
#     {"$match": { "dataset_id": 1 } },
#     { "$project":
#         {"dataset_id": 1, "max_timestamp": { "$max": "$timestamp" }}
#     }
# ])
#
# // max heart rate in all DATASETS documents
# db.DATASETS.aggregate([
#     { "$project":
#         {"dataset_id": 1, "max_heart_rate": { "$max": "$heart_rate" }}
#     }
# ])
#
# // max heart rate by dataset id
# db.DATASETS.aggregate([
#     {"$match": { "dataset_id": 1 } },
#     { "$project":
#         {"dataset_id": 1, "max_heart_rate": { "$max": "$heart_rate" }}
#     }
# ])
#
# // max sweat in all DATASETS documents
# db.DATASETS.aggregate([
#     { "$project":
#         {"dataset_id": 1, "max_sweat": { "$max": "$sweat" }}
#     }
# ])
#
# // max sweat rate by dataset id
# db.DATASETS.aggregate([
#     {"$match": { "dataset_id": 1 } },
#     { "$project":
#         {"dataset_id": 1, "max_sweat": { "$max": "$sweat" }}
#     }
# ])
#
# // min timestamp in all DATASETS documents
# db.DATASETS.aggregate([
#     { "$project":
#         {"dataset_id": 1, "min_timestamp": { "$min": "$timestamp" }}
#     }
# ])
#
# // min timestamp by dataset id
# db.DATASETS.aggregate([
#     {"$match": { "dataset_id": 1 } },
#     { "$project":
#         {"dataset_id": 1, "min_timestamp": { "$min": "$timestamp" }}
#     }
# ])
#
# // min heart rate in all DATASETS documents
# db.DATASETS.aggregate([
#     { "$project":
#         {"dataset_id": 1, "min_heart_rate": { "$min": "$heart_rate" }}
#     }
# ])
#
# // min heart rate by dataset id
# db.DATASETS.aggregate([
#     {"$match": { "dataset_id": 1 } },
#     { "$project":
#         {"dataset_id": 1, "min_heart_rate": { "$min": "$heart_rate" }}
#     }
# ])
#
# // min sweat in all DATASETS documents
# db.DATASETS.aggregate([
#     { "$project":
#         {"dataset_id": 1, "min_sweat": { "$min": "$sweat" }}
#     }
# ])
#
# // min sweat rate by dataset id
# db.DATASETS.aggregate([
#     {"$match": { "dataset_id": 1 } },
#     { "$project":
#         {"dataset_id": 1, "min_sweat": { "$min": "$sweat" }}
#     }
# ])
#


@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("name"):
        return redirect("/login")
    return {"server_data": dumps(all_bio_data)}


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        user_name = request.form.get("name")
        user_email = request.form.get("email")
        user_pw = request.form.get("password")

        if users_data.find_one({"email": user_email}) is not None:
            return render_template("registerFail.html")
        else:
            encrypted_password = sha256_crypt.hash(user_pw)
            new_user = {
                "name": user_name,
                "email": user_email,
                "password": encrypted_password
            }
            users_data.insert_one(new_user)

            fetched_user = users_data.find_one({"email": user_email})
            session["name"] = fetched_user["_id"]

            return render_template("registerSuccess.html")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_email = request.form.get("email")
        user_pw = request.form.get("password")
        fetched_user = users_data.find_one({"email": user_email})

        if fetched_user is None or not sha256_crypt.verify(user_pw, fetched_user['password']):
            print("Incorrect login details")
            return render_template("loginFail.html")
        else:
            print("Logged in successfully")
            session["name"] = fetched_user["_id"]

        return render_template("loginSuccess.html")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5000)