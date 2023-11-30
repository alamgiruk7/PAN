from flask import Flask
from flask_cors import CORS
from app.extensions import mongo, build_db_uri
from app import config as CONF

# Blueprints
from app.blueprints.news import bp as news_bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config["MONGO_URI"] = build_db_uri(**CONF.DB_CREDENTIALS)
    app.config["SECRET_KEY"] = CONF.SECRET_KEY

    mongo.init_app(app)

    app.register_blueprint(news_bp)

    return app
