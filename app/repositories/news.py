from datetime import datetime
from app.extensions import mongo
from pymongo.client_session import ClientSession
from bson import json_util
import json


class News:
    def __init__(
        self,
        title: str = None,
        content: str = None,
        source: str = None,
        genre: str = None,
        authors: str = None,
        tags: str = None,
        language: str = None,
        media_origin: str = None,
        article_id: str = None,
        articlePubDate: datetime = None,
        feedBuildDate: datetime = None,
    ) -> None:
        self.__title = title
        self.__content = content
        self.__source = source
        self.__genre = genre
        self.__authors = authors
        self.__tags = tags
        self.__language = language
        self.__media_origin = media_origin
        self.__article_id = article_id
        self.__articlePubDate = articlePubDate
        self.__feedBuildDate = feedBuildDate

    def add_document(self, session: ClientSession):
        try:
            doc = mongo.db.news.insert_one(
                {
                    "title": self.__title,
                    "content": self.__content,
                    "source": self.__source,
                    "genre": self.__genre,
                    "authors": self.__authors,
                    "tags": self.__tags,
                    "language": self.__language,
                    "media_origin": self.__media_origin,
                    "article_id": self.__article_id,
                    "articlePubDate": self.__articlePubDate,
                    "feedBuildDate": self.__feedBuildDate,
                },
                session=session,
            )

            return json.loads(json_util.dumps(doc.inserted_id))

        except Exception as e:
            raise e

    @staticmethod
    def filter_documents(
        session: ClientSession,
        search_query: str = None,
        sources: list = None,
        genres: list = None,
        datetime: datetime = None,
    ):
        pipeline = []

        match_query = {}
        if search_query:
            match_search_query = {"$or": []}
            match_search_query["$or"].append(
                {
                    "title": {"$regex": f"{search_query}", "$options": "i"},
                }
            )
            match_search_query["$or"].append(
                {
                    "content": {"$regex": f"{search_query}", "$options": "i"},
                }
            )
        pipeline.append({"$match": match_search_query})

        if datetime:
            match_query["articlePubDate"] = {"$gte": datetime}
        if sources or genres:
            match_query["$or"] = []
        if sources:
            match_query["$or"].append({"source": {"$in": sources}})
        if genres:
            match_query["$or"].append({"genre": {"$in": genres}})
        pipeline.append({"$match": match_query})

        # group = [
        #     {
        #         "$group": {
        #             "_id": {"source": "$source", "genre": "$genre"},
        #             "count": {"$sum": 1},
        #             "articles": {"$push": "$$ROOT"},
        #         }
        #     }
        # ]
        # pipeline.extend(group)

        # sort = [{"$sort": {"_id.source": 1, "_id.genre": 1}}]
        # pipeline.extend(sort)

        result = list(mongo.db.news.aggregate(pipeline=pipeline, session=session))

        return result
