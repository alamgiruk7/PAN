from flask_pymongo import PyMongo


mongo = PyMongo()


def build_db_uri(
    DB_USER: str = None,
    DB_PW: str = None,
    DB_HOST: str = None,
    DB_PORT: int = None,
    DB_NAME: str = None,
    LOCAL_DB: bool = True,
) -> str:
    return (
        "mongodb+srv://{}:{}@{}/{}/?retryWrites=true&w=majority".format(
            DB_USER, DB_PW, DB_HOST, DB_NAME
        )
        if not LOCAL_DB
        else "mongodb://{}:{}/{}".format(DB_HOST, DB_PORT, DB_NAME)
    )
