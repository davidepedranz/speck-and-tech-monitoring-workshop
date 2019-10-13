from typing import Tuple
from uuid import uuid4, UUID

import pytest

from app.models.stats import Stats
from app.models.todo import Todo
from app.repository.base import Repository
from app.repository.instrumented import InstrumentedRepository
from app.repository.memory import InMemoryRepository
from app.repository.postgresql import PostgreSQLRepository


def pytest_generate_tests(metafunc):
    if "repository" in metafunc.fixturenames:
        metafunc.parametrize(
            "repository",
            ["in_memory", "postgresql", "instrumented_in_memory"],
            indirect=True,
        )


@pytest.fixture
def in_memory_repository():
    yield InMemoryRepository()


@pytest.fixture
def postgresql_repository():
    repository = PostgreSQLRepository.factory()
    repository.connect()
    repository.initialize()
    yield repository
    repository.disconnect()


# noinspection PyProtectedMember
@pytest.fixture
def repository(request, in_memory_repository, postgresql_repository):
    if request.param == "in_memory":
        repository = in_memory_repository
    elif request.param == "postgresql":
        repository = postgresql_repository
    elif request.param == "instrumented_in_memory":
        repository = InstrumentedRepository(in_memory_repository)
    else:
        raise ValueError("Invalid repository in test configuration")
    repository._clean()
    yield repository
    repository._clean()


def test_stats_empty(repository: Repository) -> None:
    stats = repository.stats()
    assert stats == Stats(active=0, inactive=0)


def test_stats(repository: Repository) -> None:
    _insert_todo(repository, "This is a Todo!")
    _insert_todo(repository, "This is a ANOTHER Todo!")
    id_3, _ = _insert_todo(repository, "This is a yet ANOTHER Todo!")
    repository.deactivate(id_3)

    stats = repository.stats()
    assert stats == Stats(active=2, inactive=1)


def test_get_not_existing_todo(repository: Repository) -> None:
    todo = repository.get(_random_id())
    assert todo is None


def test_get_existing_todo(repository: Repository) -> None:
    id_1, text_1 = _insert_todo(repository, "This is a Todo!")
    _insert_todo(repository, "This is a ANOTHER Todo!")

    todo = repository.get(id_1)
    assert todo == Todo(id=id_1, text=text_1, active=True)


def test_get_empty_list(repository: Repository) -> None:
    todos = repository.list()
    assert todos == ()


def test_get_list_with_single_todo(repository: Repository) -> None:
    id_, text = _insert_todo(repository, "This is a Todo!")

    todos = repository.list()
    assert todos == (Todo(id=id_, text=text, active=True),)


def test_get_list_with_multiple_todos(repository: Repository) -> None:
    id_1, text_1 = _insert_todo(repository, "This is a Todo!")
    id_2, text_2 = _insert_todo(repository, "This is a ANOTHER Todo!")

    todos = repository.list()
    assert todos == tuple(
        sorted(
            (
                Todo(id=id_1, text=text_1, active=True),
                Todo(id=id_2, text=text_2, active=True),
            )
        )
    )


def test_edit_text_not_existing_todo(repository: Repository) -> None:
    id_, text = _insert_todo(repository, "This is a Todo!")

    result = repository.edit_text(_random_id(), "Hello World")
    assert not result

    todo = repository.get(id_)
    assert todo == Todo(id=id_, text=text, active=True)


def test_edit_text_existing_todo(repository: Repository) -> None:
    id_1, text_1 = _insert_todo(repository, "This is a Todo!")
    id_2, text_2 = _insert_todo(repository, "This is a ANOTHER Todo!")

    result = repository.edit_text(id_2, "Hello")
    assert result

    todos = repository.list()
    assert todos == tuple(
        sorted(
            (
                Todo(id=id_1, text=text_1, active=True),
                Todo(id=id_2, text="Hello", active=True),
            )
        )
    )


def test_mark_complete_not_existing_todo(repository: Repository) -> None:
    id_, text = _insert_todo(repository, "This is a Todo!")

    result = repository.deactivate(_random_id())
    assert not result

    todo = repository.get(id_)
    assert todo == Todo(id=id_, text=text, active=True)


def test_mark_complete_existing_todo(repository: Repository) -> None:
    id_1, text_1 = _insert_todo(repository, "This is a Todo!")
    id_2, text_2 = _insert_todo(repository, "This is a ANOTHER Todo!")

    result = repository.deactivate(id_2)
    assert result

    todos = repository.list()
    assert todos == tuple(
        sorted(
            (
                Todo(id=id_1, text=text_1, active=True),
                Todo(id=id_2, text=text_2, active=False),
            )
        )
    )


def test_mark_incomplete_not_existing_todo(repository: Repository) -> None:
    id_, text = _insert_todo(repository, "This is a Todo!")

    result = repository.activate(_random_id())
    assert not result

    todo = repository.get(id_)
    assert todo == Todo(id=id_, text=text, active=True)


def test_mark_incomplete_existing_todo(repository: Repository) -> None:
    id_1, text_1 = _insert_todo(repository, "This is a Todo!")
    id_2, text_2 = _insert_todo(repository, "This is a ANOTHER Todo!")

    repository.deactivate(id_2)
    result = repository.activate(id_2)
    assert result

    todos = repository.list()
    assert todos == tuple(
        sorted(
            (
                Todo(id=id_1, text=text_1, active=True),
                Todo(id=id_2, text=text_2, active=True),
            )
        )
    )


def test_delete_not_existing_todo(repository: Repository) -> None:
    id_, text = _insert_todo(repository, "This is a Todo!")

    result = repository.delete(_random_id())
    assert not result

    todo = repository.get(id_)
    assert todo == Todo(id=id_, text=text, active=True)


def test_delete_existing_todo(repository: Repository) -> None:
    id_1, _ = _insert_todo(repository, "This is a Todo!")
    id_2, text_2 = _insert_todo(repository, "This is a ANOTHER Todo!")

    result = repository.delete(id_1)
    assert result

    todos = repository.list()
    assert todos == (Todo(id=id_2, text=text_2, active=True),)


def _random_id() -> UUID:
    return uuid4()


def _insert_todo(repository: Repository, text: str) -> Tuple[UUID, str]:
    id_ = repository.insert(text)
    return id_, text
