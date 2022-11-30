import json
import random
import string
import time
import certifi
import threading
import pandas as pd
import plotly.express as px
import pymongo
import redis

from datetime import timedelta, date
from flask_restx import Api, Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import verify_jwt_in_request
from flask_jwt_extended import get_jwt
from bson.json_util import dumps, loads
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from urllib.parse import quote_plus
from flask import Flask, redirect, render_template, request, session, jsonify
from flask_session import Session
from flask_cors import CORS
from flask_redoc import Redoc
from passlib.hash import sha256_crypt
from pymongo import MongoClient
import jinja2

with open("config/.secrets.json") as config_file:
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
app.jinja_env.filters['zip'] = zip

ACCESS_EXPIRES = timedelta(hours=1)

# Set up the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_EXPIRES
jwt = JWTManager(app)

# Setup our redis connection for storing the blocklisted tokens. You will probably
# want your redis instance configured to persist data to disk, so that a restart
# does not cause your application to forget that a JWT was revoked.
jwt_redis_blocklist = redis.StrictRedis(
    host="localhost", port=6379, db=0, decode_responses=True
)


# Callback function to check if a JWT exists in the redis blocklist
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_redis = jwt_redis_blocklist.get(jti)
    print(token_in_redis)
    return token_in_redis is not None


api = Api(app)

redoc = Redoc(app, '../postman/schemas/index.json')
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


# @app.route("/", methods=["GET", "POST"])
# def index():
#     if not session.get("name"):
#         return redirect("/authenticate")
#     return redirect("/my_reviews")


@api.route('/register')
class Register(Resource):
    def post(self):
        user_name = request.form.get("name")
        user_email = request.form.get("email")
        user_pw = request.form.get("password")

        if users_data.find_one({"email": user_email}) is not None:
            return {"message": "User already exists", "success": "false", "data": {}}, 401

        encrypted_password = sha256_crypt.hash(user_pw)
        new_user = {
            "name": user_name,
            "email": user_email,
            "password": encrypted_password
        }
        users_data.insert_one(new_user)

        fetched_user = users_data.find_one({"email": user_email})
        access_token = create_access_token(identity=str(fetched_user['_id']))

        return {"message": "Registration Successful", "success": "true", "data": {"access_token": access_token}}, 200


@api.route('/login')
class Login(Resource):
    def post(self):
        user_email = request.form.get("email")
        user_pw = request.form.get("password")
        fetched_user = users_data.find_one({"email": user_email})

        if fetched_user is None or not sha256_crypt.verify(user_pw, fetched_user['password']):
            return {"message": "Incorrect login details", "success": "false", "data": {}}, 403
        else:
            access_token = create_access_token(identity=str(fetched_user['_id']))
            print(access_token)
            return {"message": "Login successful", "success": "true", "data": {"access_token": access_token, "name": fetched_user['name']}}, 200



# Endpoint for revoking the current users access token. Save the JWTs unique
# identifier (jti) in redis. Also set a Time to Live (TTL)  when storing the JWT
# so that it will automatically be cleared out of redis after the token expires.

@api.route("/logout")
class Logout(Resource):
    @jwt_required()
    def delete(self):
        jti = get_jwt()["jti"]
        jwt_redis_blocklist.set(jti, "", ex=ACCESS_EXPIRES)
        return {"message": "Logout successful", "success": "true", "data": {}}


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
    # biodata = bio_data.find({"dataset_id": dataset_id})
    # dataset_id = "ipbtxxjifiugghkkiirjzhshlzjeibvjbijrogxaldghavaivxa"

    # timestamps = []
    # heart_rates = []
    # sweats = []

    data = bio_data.find({"dataset_id": dataset_id})

    heart_graphs = []
    sweat_graphs = []

    count = 0

    print(data)

    for x in data:

        timestamps = x["timestamp"]
        heart_rates = x["heart_rate"]
        sweats = x["sweat"]

        print(timestamps)
        print(heart_rates)
        print(sweat)

        data_ = {"timestamps": timestamps, "heart_rate": heart_rates, "sweats": sweats}

        df = pd.DataFrame(data_, columns=['timestamps', 'heart_rate', 'sweats'])

        # heart rates data visualization
        fig = px.line(df, x="timestamps", y="heart_rate", title='Graph Of Users Heart Rates Through The Movie',
                      labels={'timestamps': 'timestamps in seconds',
                              'heart_rate': 'heart rates in bpm'})
        div = fig.to_html(full_html=False)

        # sweat data visualization
        fig2 = px.line(df, x="timestamps", y="sweats", title='Graph Of Users Sweat Through The Movie',
                      labels={'timestamps': 'timestamps in seconds',
                              'sweats': 'sweat'})
        div2 = fig2.to_html(full_html=False)

        heart_graphs.append(div)
        sweat_graphs.append(div2)

        count = count + 1
        print(count)

    return render_template("biodata.html", biodata=data, heartgraphs=heart_graphs, sweatgraphs=sweat_graphs)


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
