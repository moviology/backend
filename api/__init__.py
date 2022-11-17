import json
import random
import string
import time
import certifi
import threading

from bson.json_util import dumps, loads
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from datetime import date
from urllib.parse import quote_plus
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from passlib.hash import sha256_crypt
from pymongo import MongoClient

with open("../config/.secrets.json") as config_file:
    config = json.load(config_file)

# with open('hello', 'r') as f:
#     print(f.read())


pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-7e0595fb-09cc-4333-b707-b20f4a6b96cd'
pnconfig.publish_key = 'pub-c-60cb8668-e930-4e11-bb2e-65996cf9d14a'
pnconfig.user_id = "Kacper-device"
pubnub = PubNub(pnconfig)

added_listener = False

my_channel = 'Moviology-Channel'

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
# max timestamp in all DATASETS documents
# db.DATASETS.aggregate([
#     { "$project":
#         {"dataset_id": 1, "max_timestamp": { "$max": "$timestamp" }}
#     }
# ])
#
# max timestamp by dataset id
# db.DATASETS.aggregate([
#     {"$match": { "dataset_id": 1 } },
#     { "$project":
#         {"dataset_id": 1, "max_timestamp": { "$max": "$timestamp" }}
#     }
# ])
#
# max heart rate in all DATASETS documents
# db.DATASETS.aggregate([
#     { "$project":
#         {"dataset_id": 1, "max_heart_rate": { "$max": "$heart_rate" }}
#     }
# ])
#
# max heart rate by dataset id
# db.DATASETS.aggregate([
#     {"$match": { "dataset_id": 1 } },
#     { "$project":
#         {"dataset_id": 1, "max_heart_rate": { "$max": "$heart_rate" }}
#     }
# ])
#
# max sweat in all DATASETS documents
# db.DATASETS.aggregate([
#     { "$project":
#         {"dataset_id": 1, "max_sweat": { "$max": "$sweat" }}
#     }
# ])
#
# max sweat rate by dataset id
# db.DATASETS.aggregate([
#     {"$match": { "dataset_id": 1 } },
#     { "$project":
#         {"dataset_id": 1, "max_sweat": { "$max": "$sweat" }}
#     }
# ])
#
# min timestamp in all DATASETS documents
# db.DATASETS.aggregate([
#     { "$project":
#         {"dataset_id": 1, "min_timestamp": { "$min": "$timestamp" }}
#     }
# ])
#
# min timestamp by dataset id
# db.DATASETS.aggregate([
#     {"$match": { "dataset_id": 1 } },
#     { "$project":
#         {"dataset_id": 1, "min_timestamp": { "$min": "$timestamp" }}
#     }
# ])
#
# min heart rate in all DATASETS documents
# db.DATASETS.aggregate([
#     { "$project":
#         {"dataset_id": 1, "min_heart_rate": { "$min": "$heart_rate" }}
#     }
# ])
#
# min heart rate by dataset id
# db.DATASETS.aggregate([
#     {"$match": { "dataset_id": 1 } },
#     { "$project":
#         {"dataset_id": 1, "min_heart_rate": { "$min": "$heart_rate" }}
#     }
# ])
#
# min sweat in all DATASETS documents
# db.DATASETS.aggregate([
#     { "$project":
#         {"dataset_id": 1, "min_sweat": { "$min": "$sweat" }}
#     }
# ])
#
# min sweat rate by dataset id
# db.DATASETS.aggregate([
#     {"$match": { "dataset_id": 1 } },
#     { "$project":
#         {"dataset_id": 1, "min_sweat": { "$min": "$sweat" }}
#     }
# ])
#
# max user_id in USERS collection
# db.USERS.aggregate([
#     {"$group": {
#         "_id": "$user_id",
#         "max_user_id": {"$max": "$user_id"}
#         }
#     },
#     {"$sort" :{"_id" :-1}},
#     {"$limit": 1}
# ])
#
# min user_id in USERS collection
# db.USERS.aggregate([
#     {"$group": {
#         "_id": "$user_id",
#         "min_user_id": {"$min": "$user_id"}
#         }
#     },
#     {"$sort" :{"_id" : 1}},
#     {"$limit": 1}
# ])

# max user_id in USERS collection

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];


class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost
        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel(my_channel).message('[{"name":"Ram", "email":"Ram@gmail.com"}, {"name":"Bob", "email":"bob32@gmail.com"}]').pn_async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        # Handle new message stored in message.message
        print(message.message)
        try:
            json_data = json.loads(message.message)
            print(json_data[0]['name'])
        except:
            print("Incorrect format")

        print(message.publisher)


@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("name"):
        return redirect("/login")
    # return {"server_data": dumps(all_bio_data)}
    return render_template("index.html")


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


@app.route("/my_reviews")
def my_reviews():
    if not session.get("name"):
        return redirect("/login")

    all_reviews = []
    user_reviews = reviews_data.aggregate([
        {"$match": {"user_id": session['name']}},
        {"$lookup": {"from": 'MOVIES', "localField": 'movie_id', "foreignField": "_id", "as": "movie_id"}},
    ])

    for review in user_reviews:
        print(review)
        try:
            print(review['movie_id'][0]['name'])
            all_reviews.append(review)
        except IndexError:
            print("Invalid variable name for movie_id")

    return render_template("reviews.html", user_reviews=all_reviews)


@app.route("/view_biodata/<dataset_id>", methods=['GET', 'POST'])
def view_biodata(dataset_id):
    biodata = bio_data.find({"dataset_id": dataset_id})
    return render_template("biodata.html", biodata=biodata)


@app.route("/book", methods=['GET', 'POST'])
def book():
    possible_genres = ["Adventure", "Comedy", "Action", "Sci-Fi"]

    if not session.get("name"):
        return redirect("/login")

    if request.method == "POST":
        name = request.form.get("name")
        genres = []
        movie_id = get_random_string(50)

        for genre in possible_genres:
            if request.form.get(genre) is not None:
                genres.append(genre)

        new_movie = {
            "_id": movie_id,
            "name": name,
            "genre": genres,
            "user_id": session["name"]
        }
        movies_data.insert_one(new_movie)

        description = request.form.get("description")
        dataset_id = get_random_string(50)

        new_review = {
            "description": description,
            "date": str(date.today()),
            "user_id": session["name"],
            "dataset_id": dataset_id,
            "movie_id": movie_id
        }
        reviews_data.insert_one(new_review)

    return render_template("bookReview.html", possibleGenres=possible_genres)


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str


if __name__ == "__main__":
    moviology_thread = threading.Thread()
    moviology_thread.start()

    if not added_listener:
        pubnub.add_listener(MySubscribeCallback())
        print(added_listener)
        added_listener = True

    pubnub.subscribe().channels(my_channel).execute()
    app.run(port=5000)
