from typing import Tuple, Optional
from uuid import UUID

from app.models.stats import Stats
from app.models.todo import Todo
from app.repository.base import Repository


# TODO (2): measure the execution time of the different database operations
class InstrumentedRepository(Repository):
    """
    Prometheus-instrumented decorator for a concrete implementation of Repository.
    Please use it as follows:
    ```
        basic_repository = ...
        instrumented_repository = InstrumentedRepository(basic_repository)
    ```
    """

    def __init__(self, repository: Repository):
        self._repository = repository

    def stats(self) -> Stats:
        return self._repository.stats()

    def get(self, id_: UUID) -> Optional[Todo]:
        return self._repository.get(id_=id_)

    def list(self) -> Tuple[Todo, ...]:
        return self._repository.list()

    def insert(self, text: str) -> UUID:
        return self._repository.insert(text=text)

    def edit_text(self, id_: UUID, text: str) -> bool:
        return self._repository.edit_text(id_=id_, text=text)

    def activate(self, id_: UUID) -> bool:
        return self._repository.activate(id_=id_)

    def deactivate(self, id_: UUID) -> bool:
        return self._repository.deactivate(id_=id_)

    def delete(self, id_: UUID) -> bool:
        return self._repository.delete(id_=id_)

    def _clean(self) -> None:
        return self._repository._clean()
