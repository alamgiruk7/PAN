from http import HTTPStatus
from flask import Blueprint, jsonify
from app.blc.news import NewsBLC
from app.extensions import mongo
from webargs.flaskparser import use_args
from webargs import fields

bp = Blueprint("news", __name__)


@bp.route("/get_news", methods=["GET"])
@use_args(
    {
        "search_query": fields.String(),
        "sources": fields.List(fields.String()),
        "genres": fields.List(fields.String()),
        "datetime": fields.DateTime(),
    },
    location="json",
)
def get_news(args: dict):
    try:
        with mongo.db.client.start_session() as session:
            result = NewsBLC.get_filtered_news(args=args, session=session)

    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.UNPROCESSABLE_ENTITY

    return jsonify(result), HTTPStatus.OK
