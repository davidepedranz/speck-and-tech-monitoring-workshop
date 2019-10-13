from http import HTTPStatus
from typing import Optional

from flask import request, Flask, Response
from prometheus_client.registry import REGISTRY


def register_prometheus(app: Flask, registry=REGISTRY) -> None:
    """
    Automatically collect and expose metrics about HTTP calls in a Flask application.
    :param app: Instance of a Flask application.
    :param registry: Metrics registry to expose, defaults to default Prometheus registry.
    """

    def after(response: Response) -> Response:
        endpoint = _get_endpoint()
        status_code = _get_status_code(response)

        # TODO (1): count the number of calls by Flask endpoint and status_code

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
