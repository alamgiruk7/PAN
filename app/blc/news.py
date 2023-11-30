from app.repositories.news import News
from pymongo.client_session import ClientSession


class NewsBLC:
    @staticmethod
    def add_document(args: dict, session: ClientSession) -> dict:
        news = News(**args)

        doc_id = news.add_document(session=session)

        return doc_id

    @staticmethod
    def get_filtered_news(args: dict, session: ClientSession) -> dict:
        news = News.filter_documents(
            session=session,
            search_query=args.get("search_query"),
            sources=args.get("sources"),
            genres=args.get("genres"),
            datetime=args.get("datetime"),
        )

        return news
