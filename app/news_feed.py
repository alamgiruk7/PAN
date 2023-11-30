import requests
from utilities import MongoDBClient
from utilities import FeedParser
from feed_urls import feed_urls
from time import time

CONNECTION_STRING = "mongodb://127.0.0.1:27017/"
DATABASE = "test_db"
COLLECTION = "test_news"


def main():
    try:
        total_time = 0
        print("Feed Ingestion has started !!!!\n\n")
        # URL to fetch XML data
        for feed in feed_urls:
            source_start_time = time()
            media_origin = feed.get("media_origin", "Unknown")
            source = feed.get("source", "Unknown")

            if "urls" in feed:
                for url_dict in feed["urls"]:
                    genre_start_time = time()
                    url = url_dict.get("url")
                    genre = url_dict.get("genre")

                    # Fetch XML data
                    response = requests.get(url)

                    if response.status_code == 200:
                        xml_data = response.text
                        json_data = FeedParser.xml_to_json(
                            media_origin, source, genre, xml_data
                        )

                        # creating an instance of MongoDB
                        mongo_client = MongoDBClient(CONNECTION_STRING, DATABASE)

                        # Inserting documents into MongoDB collection
                        _ = mongo_client.insert_documents(COLLECTION, json_data)

                        genre_stop_time = time()
                        genre_time = genre_stop_time - genre_start_time
                        print(
                            f'Feed of "{source}", "{genre.upper()}" completed in {round(genre_time, 2)} seconds'
                        )

                source_stop_time = time()
                source_time = source_stop_time - source_start_time
                total_time += source_time
                print(
                    "\n\n######################################################################"
                )
                print(
                    f'"Ingestion of {source}" all genres completed in {round(source_time, 2)} seconds'
                )
                print(
                    "######################################################################\n\n"
                )

            else:
                print("Failed to fetch XML data. Status code: ", response.status_code)
        print(
            "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        )
        print(
            f"Ingestion of all Media-Feed completed in {round(total_time, 2)} seconds"
        )
        print(
            "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n"
        )
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
