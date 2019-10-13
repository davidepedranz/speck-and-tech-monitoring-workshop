from typing import NamedTuple
from uuid import UUID


class Todo(NamedTuple):
    id: UUID
    text: str
    active: bool
