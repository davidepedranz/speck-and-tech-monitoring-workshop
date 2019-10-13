from typing import Tuple, Optional
from uuid import UUID

from app.models.stats import Stats
from app.models.todo import Todo


class Repository:
    """
    Repository for Todos: define methods to retrieve, insert, modify and delete Todos.
    """

    def stats(self) -> Stats:
        """
        Retrieve statistics about the number of Todos stored.
        :return: Todos statistics.
        """
        raise NotImplementedError  # pragma: nocover

    def get(self, id_: UUID) -> Optional[Todo]:
        """
        Retrieve a Todo by its ID.
        :param id_: ID of the Todo.
        :return: The Todo if existing, None otherwise.
        """
        raise NotImplementedError  # pragma: nocover

    def list(self) -> Tuple[Todo, ...]:
        """
        Retrieve all stored Todos.
        :return: Tuple of all Todos, ordered by increasing ID.
        """
        raise NotImplementedError  # pragma: nocover

    def insert(self, text: str) -> UUID:
        """
        Insert a new active Todo.
        :param text: Text for the Todo to insert.
        :return: ID generated for the Todo.
        """
        raise NotImplementedError  # pragma: nocover

    def edit_text(self, id_: UUID, text: str) -> bool:
        """
        Edit the text for an existing Todo.
        :param id_: ID of the Todo to update.
        :param text: New text for the Todo.
        :return: True if the Todo was found and correctly updated, false otherwise.
        """
        raise NotImplementedError  # pragma: nocover

    def activate(self, id_: UUID) -> bool:
        """
        Mark an existing Todo as active.
        :param id_: ID of the Todo to update.
        :return: True if the Todo was found and correctly updated, false otherwise.
        """
        raise NotImplementedError  # pragma: nocover

    def deactivate(self, id_: UUID) -> bool:
        """
        Mark an existing Todo as not active.
        :param id_: ID of the Todo to update.
        :return: True if the Todo was found and correctly updated, false otherwise.
        """
        raise NotImplementedError  # pragma: nocover

    def delete(self, id_: UUID) -> bool:
        """
        Delete an existing Todo.
        :param id_: ID of the Todo to delete.
        :return: True if the Todo was found and correctly deleted, false otherwise.
        """
        raise NotImplementedError  # pragma: nocover

    def _clean(self) -> None:
        """
        Delete all Todos. Please use this method for tests only!
        """
        raise NotImplementedError  # pragma: nocover
