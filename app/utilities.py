import json
import xmltodict
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient


class MongoDBClient:
    def __init__(self, connection_string, db_name):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]

    def insert_documents(self, collection_name, document_list):
        collection = self.db[collection_name]
        # return collection.insert_many(document_list)
        for document in document_list:
            collection.update_one(
                {"_id": document["_id"]}, {"$set": document}, upsert=True
            )
        return

    def find_documents(self, collection_name, query, keys_to_include={}):
        collection = self.db[collection_name]
        return collection.find(query, keys_to_include).limit(10)

    def find_documents_count(self, collection_name, query):
        collection = self.db[collection_name]
        return collection.count_documents(query)


class FeedParser:
    """A class to parse XML feed data"""

    @staticmethod
    def xml_to_json(media_origin, source, genre, xml_data):
        """A method to convert XML data to JSON"""

        parsed_list = []
        # Parse XML to Python dictionary
        parsed_data = xmltodict.parse(xml_data)

        # Convert to JSON
        json_data = json.dumps(parsed_data, indent=2, ensure_ascii=False)

        # Parse the JSON data to remove HTML tags from the 'description' field
        parsed_json = json.loads(json_data)

        language = (
            parsed_json.get("rss", "unknown")
            .get("channel", "unknown")
            .get("language", "unknown")
        )

        for item in parsed_json.get("rss").get("channel").get("item"):
            # Remove HTML tags from the 'description' field
            if "description" in item and media_origin == "foreign":
                soup = BeautifulSoup(item.get("description"), "html.parser")
                item["description"] = soup.get_text()
            elif "content:encoded" in item and media_origin == "local":
                soup = BeautifulSoup(item.get("content:encoded"), "html.parser")
                item["content:encoded"] = soup.get_text()

            parsed_list.append(item)

        # extracting feed build date to be used with every article in mongo document
        feedBuildDate = parsed_json.get("rss").get("channel").get("lastBuildDate")

        mongo_docs_list = FeedParser.prepare_news_documents(
            media_origin, source, genre, language, feedBuildDate, parsed_list
        )

        return mongo_docs_list

    @staticmethod
    def prepare_news_documents(
        media_origin, source, genre, language, feedBuildDate, parsed_list
    ):
        """Method to prepare the news documents for mongoDB"""
        document_list = []

        parsed_build_date = (
            datetime.strptime(feedBuildDate, "%a, %d %b %Y %H:%M:%S GMT")
            if media_origin == "foreign"
            else datetime.strptime(feedBuildDate, "%a, %d %b %y %H:%M:%S %z")
        )

        feed_build_date_tuple = FeedParser.create_date_tuple(parsed_build_date)

        for item in parsed_list:
            articlePubDate = item.get("pubDate")
            if articlePubDate:
                try:
                    parsed_pubDate = (
                        datetime.strptime(articlePubDate, "%a, %d %b %Y %H:%M:%S GMT")
                        if media_origin == "foreign"
                        else datetime.strptime(
                            articlePubDate, "%a, %d %b %y %H:%M:%S %z"
                        )
                    )

                    pub_date_tuple = FeedParser.create_date_tuple(parsed_pubDate)
                except Exception:
                    parsed_pubDate = None

            document = {}
            document["_id"] = item.get("link")
            document["media_origin"] = media_origin
            document["source"] = source
            document["genre"] = genre
            document["language"] = language
            document["feedBuildDate"] = datetime(*feed_build_date_tuple)
            document["title"] = item.get("title")
            document["content"] = (
                item.get("description")
                if media_origin == "foreign"
                else item.get("content:encoded")
            )
            document["articlePubDate"] = (
                datetime(*pub_date_tuple) if articlePubDate else None
            )
            document["tags"] = item.get("category")
            document["article_id"] = item.get("guid").get("#text")
            document["authors"] = item.get("author", source)

            document_list.append(document)

        return document_list

    @staticmethod
    def create_date_tuple(parsed_date):
        # Extract the individual date and time components
        year = parsed_date.year
        month = parsed_date.month
        day = parsed_date.day
        hour = parsed_date.hour
        minute = parsed_date.minute
        second = parsed_date.second

        return (
            year,
            month,
            day,
            hour,
            minute,
            second,
        )
