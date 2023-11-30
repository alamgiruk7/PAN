import os


SECRET_KEY = os.environ.get("SECRET_KEY")

DB_CREDENTIALS = {
    "DB_HOST": os.environ.get("DB_HOST"),
    "DB_PORT": os.environ.get("DB_PORT"),
    "DB_USER": os.environ.get("DB_USER"),
    "DB_PW": os.environ.get("DB_PW"),
    "DB_NAME": os.environ.get("DB_NAME"),
}
