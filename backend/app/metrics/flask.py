from http import HTTPStatus
from typing import Optional

from flask import request, Flask, Response
from prometheus_client import Counter
from prometheus_client.registry import REGISTRY


def register_prometheus(app: Flask, registry=REGISTRY) -> None:
    """
    Automatically collect and expose metrics about HTTP calls in a Flask application.
    :param app: Instance of a Flask application.
    :param registry: Metrics registry to expose, defaults to default Prometheus registry.
    """

    counter = Counter(
        namespace="app",
        subsystem="flask",
        name="http_request",
        unit="total",
        documentation="Total number of HTTP requests handled by Flask",
        labelnames=("endpoint", "status_code"),
        registry=registry,
    )

    def after(response: Response) -> Response:
        endpoint = _get_endpoint()
        status_code = _get_status_code(response)

        # TASK (1): count the number of calls by Flask endpoint and status_code
        # SOLUTION: we create a new `Counter` object and increment it with the correct labels
        #           (one for the endpoint and one for the status_code) for each request
        counter.labels(endpoint=endpoint, status_code=status_code).inc()

        return response

    def _get_endpoint() -> Optional[str]:
        """
        Extracts the endpoint from a Flask request.
        :return: Flask endpoint.
        """
        if request.endpoint is None:
            return None
        return request.endpoint.split(".")[-1]

    def _get_status_code(response: Response) -> int:
        """
        Extracts the HTTP status code from a Flask response.
        :param response: Flask response.
        :return: HTTP status code.
        """
        status_code = response.status_code
        if isinstance(status_code, HTTPStatus):
            return status_code.value
        else:
            return status_code

    # Flask will execute the `after` function after serving each request
    app.after_request(after)
