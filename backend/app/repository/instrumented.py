from typing import Tuple, Optional
from uuid import UUID

from prometheus_client import Histogram

from app.models.stats import Stats
from app.models.todo import Todo
from app.repository.base import Repository

# TASK (2): measure the execution time of the different database operations
# SOLUTION: we create a new `Histogram` object and wrap each call with the `.time()` context
#           manager to measure the execution time; we use a label to identify the operation
class InstrumentedRepository(Repository):
    """
    Prometheus-instrumented decorator for a concrete implementation of Repository.
    Please use it as follows:
    ```
        basic_repository = ...
        instrumented_repository = InstrumentedRepository(basic_repository)
    ```
    """

    _HISTOGRAM = Histogram(
        namespace="app",
        subsystem="repository",
        name="query_duration",
        unit="seconds",
        documentation="Time required to handle a query to the Todos repository",
        labelnames=("query",),
    )

    def __init__(self, repository: Repository):
        self._repository = repository

    def stats(self) -> Stats:
        with self._HISTOGRAM.labels(query="stats").time():
            return self._repository.stats()

    def get(self, id_: UUID) -> Optional[Todo]:
        with self._HISTOGRAM.labels(query="get").time():
            return self._repository.get(id_=id_)

    def list(self) -> Tuple[Todo, ...]:
        with self._HISTOGRAM.labels(query="list").time():
            return self._repository.list()

    def insert(self, text: str) -> UUID:
        with self._HISTOGRAM.labels(query="insert").time():
            return self._repository.insert(text=text)

    def edit_text(self, id_: UUID, text: str) -> bool:
        with self._HISTOGRAM.labels(query="edit_text").time():
            return self._repository.edit_text(id_=id_, text=text)

    def activate(self, id_: UUID) -> bool:
        with self._HISTOGRAM.labels(query="activate").time():
            return self._repository.activate(id_=id_)

    def deactivate(self, id_: UUID) -> bool:
        with self._HISTOGRAM.labels(query="deactivate").time():
            return self._repository.deactivate(id_=id_)

    def delete(self, id_: UUID) -> bool:
        with self._HISTOGRAM.labels(query="delete").time():
            return self._repository.delete(id_=id_)

    def _clean(self) -> None:
        with self._HISTOGRAM.labels(query="_clean").time():
            return self._repository._clean()
