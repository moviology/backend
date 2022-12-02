from pymongo import MongoClient
from urllib.parse import quote_plus
import json
import certifi
import plotly.express as px
import pandas as pd

from pymongo.errors import WriteConcernError, WriteError

with open("C:/Users/conor/PycharmProjects/backend/config/.secrets.json") as config_file:
    config = json.load(config_file)

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


timestamps = []
heart_rates = []
sweats = []
dataset_id = "ipbtxxjifiugghkkiirjzhshlzjeibvjbijrogxaldghavaivxa"
data = bio_data.find({"dataset_id": dataset_id})

for x in data:
    timestamps = x["timestamp"]
    heart_rates = x["heart_rate"]
    sweats = x["sweat"]

data_ = {"timestamps": timestamps, "heart_rate": heart_rates, "sweats": sweats}

df = pd.DataFrame(data_, columns = ['timestamps', 'heart_rate', 'sweats'])
print(df.head())

fig = px.line(df, x="timestamps", y="heart_rate", title='Graph Of Users Heart Rates Through The Movie',
              labels={'timestamps': 'timestamps in seconds',
                      'heart_rate': 'heart rates in bpm'})
fig.show()
df.to_csv('data_for_graph.csv')
