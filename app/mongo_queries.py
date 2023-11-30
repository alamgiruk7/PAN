import json
from utilities import MongoDBClient
from datetime import datetime, timedelta
from utilities import FeedParser


CONNECTION_STRING = "mongodb://127.0.0.1:27017/"
DATABASE = "pan"
COLLECTION = "news"


# creating an instance of MongoDB
mongo_client = MongoDBClient(CONNECTION_STRING, DATABASE)
mongo_client.db[]

# Below are the different queries required for different scenarios

# Query for documents of any particular Source
# query = '{"$or": [{"source": "AP-News"}, {"source": "Express-Tribune"}]}'

# Query for documents of any particular Source with particular genre
query = {"$and": [{"genre": "top-news"}, {"source": "Express-Tribune"}]}

# Latest news from all media-sources
query = {"genre": "top-news"}

# Query to retrieve last 24 hours documents
now = datetime.now()
current_time_tuple = FeedParser.create_date_tuple(now)
now = datetime(*current_time_tuple)
twenty_four_hours_ago = now - timedelta(hours=24)
query = {"articlePubDate": {"$gt": twenty_four_hours_ago}}

# Query to retrieve last 24 hours documents of specific sources and genres with specific output
twentyFourHoursAgo = datetime(2023, 11, 7, 9, 36, 20)
query = {
    "$and": [
        {"genre": "top-news"},
        {"source": "Express-Tribune"},
        {"articlePubDate": {"$gt": twentyFourHoursAgo}},
    ],
}

keys_to_include = {"title": 1, "source": 1, "genre": 1, "content": 1}

# query = json.loads(query)
results = mongo_client.find_documents(COLLECTION, query, keys_to_include)
for doc in results:
    print(doc)

count = mongo_client.find_documents_count(COLLECTION, query)
print(f"\n\nTotal count of Documents: {count}")
