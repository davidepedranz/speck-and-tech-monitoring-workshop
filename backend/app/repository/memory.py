from typing import Tuple, Optional, Dict, Callable
from uuid import UUID, uuid1

from app.models.stats import Stats
from app.models.todo import Todo
from app.repository.base import Repository


class InMemoryRepository(Repository):
    """
    In-memory implementation of a Todos repository.
    """

    def __init__(self):
        self._todos: Dict[UUID, Todo] = {}

    def stats(self) -> Stats:
        todos = self.list()
        return Stats(
            active=len(list(filter(lambda todo: todo.active, todos))),
            inactive=len(list(filter(lambda todo: not todo.active, todos))),
        )

    def get(self, id_: UUID) -> Optional[Todo]:
        return self._todos.get(id_)

    def list(self) -> Tuple[Todo, ...]:
        return tuple(sorted(self._todos.values()))

    def insert(self, text: str) -> UUID:
        id_ = uuid1()
        todo = Todo(id=id_, text=text, active=True)
        assert self._todos.get(id_) is None
        self._todos[id_] = todo
        return id_

    def edit_text(self, id_: UUID, text: str) -> bool:
        delta = lambda todo: Todo(id=id_, text=text, active=todo.active)
        return self._update(id_=id_, delta=delta)

    def activate(self, id_: UUID) -> bool:
        delta = lambda todo: Todo(id=id_, text=todo.text, active=True)
        return self._update(id_=id_, delta=delta)

    def deactivate(self, id_: UUID) -> bool:
        delta = lambda todo: Todo(id=id_, text=todo.text, active=False)
        return self._update(id_=id_, delta=delta)

    def delete(self, id_: UUID) -> bool:
        result = self._todos.pop(id_, None)
        return result is not None

    def _update(self, id_: UUID, delta: Callable[[Todo], Todo]):
        old_todo = self._todos.get(id_)
        if old_todo is None:
            return False
        else:
            new_todo = delta(old_todo)
            self._todos[id_] = new_todo
            return True

    def _clean(self) -> None:
        self._todos = {}
