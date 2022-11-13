from flask import Flask, redirect, render_template, request, session, url_for
from pymongo import MongoClient
from flask_session import Session
from urllib.parse import quote_plus
from bson.json_util import dumps
import json
import certifi

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
# client object for a MongoDB instance called client, which allows you to connect and interact with your MongoDB server
# When you instantiate the MongoClient(), you pass it the host of your MongoDB server, which is mongodb+srv...... in our case

db = client.Moviology  # You then use the client instance to create a MongoDB database called moviology_db and save a
# reference to it in a variable called db.

bio_data = db.DATASETS  # Creating new collection on the database using the db variable.
movies_data = db.MOVIES  # Collections store a group of documents in MongoDB, like tables in relational databases.
reviews_data = db.REVIEWS
users_data = db.USERS

# CREATING TEST DATA
testData = {
    "dataset_id": 3,
    "timestamp": [3, 6, 9, 12, 15],
    "heart_rate": [100, 120, 109, 112],
    "sweat": [0, 5, 6, 12],
    "machine_id": 128219,
}

# FETCHING ALL DATA FROM ALL 4 TABLES
all_bio_data = bio_data.find()
all_movies_data = movies_data.find()
all_reviews_data = reviews_data.find()
all_users_data = users_data.find()

# INSERTING TEST DATA INTO 'DATASETS' DATABASE
bio_data.insert_one(testData)

# ITERATING THROUGH EACH ELEMENT IN all_bio_data
# for bioentry in all_bio_data:
#     #bioentry is dictionary
#     print(bioentry['machine_id'])
#     print(bioentry.items())

# PRINTING DATA FROM ALL TABLES IN JSON FORMAT
print("Biometric data" + dumps(all_bio_data))
print("Movie data" + dumps(all_movies_data))
print("Review data" + dumps(all_reviews_data))
print("User data" + dumps(all_users_data))

print("\nFinding many entries that share common value for variable")
for entry in bio_data.find({"machine_id": 128219}):  # finding many documents
    print(entry)

print("\nCounting entries")
print(bio_data.count_documents({"machine_id": 128219}))

# GETTING REVIEWS FOR A SINGLE MOVIE DIRECETOR USER
testUser = users_data.find_one({"name": "kacper"})
testUserId = testUser['user_id']
print(f"\nUser name: {testUser['name']}")
testReviews = reviews_data.find_one({"user_id": testUserId})
print(f"\nReview description: {testReviews['description']}")
testMovieId = testReviews['movie_id']
testMovie = movies_data.find_one({"movie_id": testMovieId})
print(f"\nMovie name: {testMovie['name']}")
testDatasetId = testReviews['dataset_id']
print(f"\nBiometric data")
testBioData = bio_data.find({"dataset_id": testDatasetId})

# ITERATING THROUGH ALL THE BIOMETRIC DATA THAT CORRESPOND TO THE SELECTED REVIEW, USING 'dataset_id' AS FOREIGN KEY
for entry in testBioData:  # finding many documents
    print(entry)







@app.route("/", methods=["GET", "POST"])
def index():
    print(bio_data.find_one({"machine_id": 842}))
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
    app.run(debug=True, port=5000)
