from http import HTTPStatus
from uuid import UUID

from flask import Blueprint, jsonify, request

from app.repository.base import Repository


def make_todos_blueprint(repository: Repository) -> Blueprint:
    """
    Create a Flask Blueprint that contains the endpoint for all Todo REST APIs.
    :param repository: Instance of a ready-to-use repository.
    :return: Flask Blueprint with Todo APIs.
    """

    blueprint = Blueprint("todos", __name__, url_prefix="/todos")

    @blueprint.route("/<id_raw>", methods=["GET"])
    def get_todo(id_raw: str):
        id_ = _parse_uuid(id_raw)
        todo = repository.get(id_)
        if todo is None:
            return "", HTTPStatus.NOT_FOUND
        else:
            return jsonify(todo._asdict())

    @blueprint.route("/", methods=["GET"])
    def list_todos():
        todos = repository.list()
        return jsonify([todo._asdict() for todo in todos])

    @blueprint.route("/", methods=["POST"])
    def create_todo():
        if not request.is_json:
            return "", HTTPStatus.UNSUPPORTED_MEDIA_TYPE
        else:
            text = request.json["text"]
            try:
                id_ = repository.insert(text=text)
                return jsonify(id=id_), HTTPStatus.CREATED
            except KeyError:
                return "", HTTPStatus.BAD_REQUEST

    @blueprint.route("/<id_raw>", methods=["PATCH"])
    def update_todo(id_raw: str):
        if not request.is_json:
            return "", HTTPStatus.UNSUPPORTED_MEDIA_TYPE
        else:
            try:
                id_ = _parse_uuid(id_raw)
                result = repository.edit_text(id_=id_, text=request.json["text"])
                return "", HTTPStatus.NO_CONTENT if result else HTTPStatus.NOT_FOUND
            except KeyError:
                return "", HTTPStatus.BAD_REQUEST

    @blueprint.route("/<id_raw>/activate", methods=["POST"])
    def activate_todo(id_raw: str):
        id_ = _parse_uuid(id_raw)
        result = repository.activate(id_=id_)
        return "", HTTPStatus.NO_CONTENT if result else HTTPStatus.NOT_FOUND

    @blueprint.route("/<id_raw>/deactivate", methods=["POST"])
    def deactivate_todo(id_raw: str):
        id_ = _parse_uuid(id_raw)
        result = repository.deactivate(id_=id_)
        return "", HTTPStatus.NO_CONTENT if result else HTTPStatus.NOT_FOUND

    @blueprint.route("/<id_raw>", methods=["DELETE"])
    def delete_todo(id_raw: str):
        id_ = _parse_uuid(id_raw)
        result = repository.delete(id_)
        return "", HTTPStatus.NO_CONTENT if result else HTTPStatus.NOT_FOUND

    return blueprint


def _parse_uuid(id_: str) -> UUID:
    try:
        return UUID(id_)
    except ValueError:
        return UUID(int=0)
