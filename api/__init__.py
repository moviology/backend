import json
import random
import string
import time
import certifi
import threading
import pymongo

from bson.json_util import dumps, loads
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from datetime import date
from urllib.parse import quote_plus
from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from flask_cors import CORS
from passlib.hash import sha256_crypt
from pymongo import MongoClient

with open("../config/.secrets.json") as config_file:
    config = json.load(config_file)

pnconfig = PNConfiguration()
pnconfig.subscribe_key = config.get("SUB_KEY")
pnconfig.publish_key = config.get("PUB_KEY")
pnconfig.user_id = config.get("UID")
pubnub = PubNub(pnconfig)

my_channel = config.get("CHANNEL")

app = Flask(__name__)
app.config["SECRET_KEY"] = config.get("SECRET_KEY")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['CORS_HEADERS'] = 'Content-Type'

Session(app)

CORS(app)

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


def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];


heart_rate = []
timestamp = []
sweat = []
machine_id = [0]


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

            # pubnub.publish().channel(my_channel).message([3, 6, 9, 9999]).pn_async(my_publish_callback)
            # pubnub.publish().channel(my_channel).message([5, 10, 15, 9999]).pn_async(my_publish_callback)
            # pubnub.publish().channel(my_channel).message([10, 20, 30, 9999]).pn_async(my_publish_callback)
            pass
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.

    def message(self, pubnub, message):
        print(message.message)
        if message.message == "stop":
            print("you have been stopped")
            latest_review = reviews_data.find_one(
                sort=[('_id', pymongo.DESCENDING)]
            )
            print(latest_review)

            new_biodata = {
                "dataset_id": latest_review["dataset_id"],
                "timestamp": timestamp,
                "heart_rate": heart_rate,
                "sweat": sweat,
                "machine_id": machine_id[0]
            }
            print("ABOUT TO SEND DATA")
            print(new_biodata)

            bio_data.insert_one(new_biodata)
        elif type(message.message) == list:
            # bio_object = json.loads(message.message)
            # heart_rate.append(bio_object[0]["biodata"][0])
            # sweat.append(bio_object[0]["biodata"][1])
            # timestamp.append(bio_object[0]["biodata"][2])
            # machine_id[0] = bio_object[0]["biodata"][3]

            heart_rate.append(message.message[0])
            sweat.append(message.message[1])

            timestamp.append(message.message[2])
            machine_id[0] = message.message[3]



            print(heart_rate)
            print(sweat)
            print(timestamp)
            print(machine_id)
        else:
            print("Invalid command")
        print(message.publisher)


@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("name"):
        return redirect("/authenticate")
    return redirect("/my_reviews")


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

            return render_template("index.html")
    return render_template("register.html")


@app.route("/authenticate", methods=["GET", "POST"])
def authenticate():
    if session.get("name"):
        return render_template("index.html")
    return render_template("authentication.html")


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

        return render_template("index.html")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")


@app.route("/my_reviews")
def my_reviews():
    if not session.get("name"):
        return redirect("/authenticate")

    all_reviews = []
    user_reviews = reviews_data.aggregate([
        {"$match": {"user_id": session['name']}},
        {"$lookup": {"from": 'MOVIES', "localField": 'movie_id', "foreignField": "_id", "as": "movie_id"}},
    ])

    for review in user_reviews:
        all_reviews.append(review)

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
    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(my_channel).execute()
    app.run(port=5000)



