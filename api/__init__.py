from flask import Flask, redirect, render_template, request, session, url_for
from pymongo import MongoClient
from flask_session import Session
from urllib.parse import quote_plus
from bson.json_util import dumps
import json
import certifi

with open("config/.secrets.json") as config_file:
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

# client object for a MongoDB instance called client, which allows you to connect and interact with your MongoDB server
# When you instantiate the MongoClient(), you pass it the host of your MongoDB server, which is mongodb+srv...... in our case

db = client.Moviology  # creating database on cluster
# You then use the client instance to create a MongoDB database called moviology_db and save a reference to it in a variable called db.

bio_data = db.DATASETS  # Creating new collection for database
# Then you create a collection called bioData on the flask_db database using the db variable.
# Collections store a group of documents in MongoDB, like tables in relational databases.

testData = {
    "timestamp": [3, 6, 9, 12, 15],
    "heart_rate": [100, 120, 109, 112],
    "sweat": [0, 5, 6, 12],
    "machine_id": 128219,
}

# print(bioData.find_one({ "machine_id": 842 }))


@app.route("/", methods=["GET", "POST"])
def index():
    all_bio_data = bio_data.find()
    print('all_bio_data', dumps(all_bio_data))
    # To display all the saved bioData, you use the find() method outside the code
    # responsible for handling POST requests, which returns all the biometric data available in the 'DATASETS' collection

    # You save the biometric data you get from the database in a variable called allBioData, and then you edit the
    # render_template() function call to pass the biometric data to the index.html template, which will be available in the
    # template in a variable called bioDatas.

    return {"server_data": dumps(all_bio_data)}


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form.get("name")
        session[
            "name"
        ] = name  # dictionary. global variable, can be accessed anywhere. created for each individual user

        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
