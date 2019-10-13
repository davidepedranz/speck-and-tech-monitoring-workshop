import os
from typing import NoReturn

from flask import Flask, Response
from prometheus_client.exposition import start_http_server as run_prometheus_http_server

from app.apis.todo import make_todos_blueprint
from app.metrics.flask import register_prometheus
from app.repository.base import Repository
from app.repository.instrumented import InstrumentedRepository
from app.repository.postgresql import PostgreSQLRepository


def main() -> None:
    run_prometheus()

    repository = PostgreSQLRepository.factory()
    repository.connect()
    try:
        repository.initialize()
        instrumented_repository = InstrumentedRepository(repository)
        register_custom_metrics(instrumented_repository)
        run_flask_app(instrumented_repository)
    finally:
        repository.disconnect()


def run_prometheus() -> None:
    host = os.environ.get("PROMETHEUS_HOST", "0.0.0.0")
    port = os.environ.get("PROMETHEUS_PORT", 6000)

    run_prometheus_http_server(addr=host, port=port)


def register_custom_metrics(repository: Repository) -> None:
    # TODO (3): register a custom collector to export the number of Todos
    #           in the database broken down by status (active vs inactive)
    # HINT: you can use `instrumented_repository.stats()` to get the Todos number
    # HINT: https://github.com/prometheus/client_python#custom-collectors
    pass


def run_flask_app(repository: Repository) -> NoReturn:
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = os.environ.get("FLASK_PORT", 5000)

    app = Flask(__name__)
    app.after_request(_cors_support)
    app.register_blueprint(make_todos_blueprint(repository))
    register_prometheus(app)
    app.run(host=host, port=port)


def _cors_support(response: Response) -> Response:
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    return response


if __name__ == "__main__":
    main()
