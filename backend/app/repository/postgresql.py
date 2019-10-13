import os
from contextlib import contextmanager
from typing import Tuple, Optional, ContextManager
from uuid import UUID

from psycopg2.extensions import connection, cursor
from psycopg2.extras import register_uuid
from psycopg2.pool import ThreadedConnectionPool

from app.models.stats import Stats
from app.models.todo import Todo
from app.repository.base import Repository
from app.utils.delay import random_delay, rare_delay


class PostgreSQLRepository(Repository):
    """
    PostgreSQL based implementation of a Todos repository.
    """

    class SQL:
        CREATE_UUID_EXTENSION = """
            CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        """

        CREATE_TABLE = """
            CREATE TABLE IF NOT EXISTS todos
            (
                id     uuid NOT NULL PRIMARY KEY DEFAULT uuid_generate_v1mc(),
                text   text NOT NULL,
                active bool NOT NULL
            );
        """

        STATS = """
            SELECT active, count(*)
            FROM todos
            GROUP BY active;
        """

        GET = """
            SELECT text, active
            FROM todos
            WHERE id = %(id)s;
        """

        LIST = """
            SELECT id, text, active
            FROM todos
            ORDER BY id;
        """

        INSERT = """
            INSERT INTO todos(text, active)
            VALUES (%(text)s, %(active)s)
            RETURNING id;
        """

        EDIT_TEXT = """
            UPDATE todos
            SET text = %(text)s
            WHERE id = %(id)s;
        """

        ACTIVATE = """
            UPDATE todos
            SET active = TRUE
            WHERE id = %(id)s;
        """

        DEACTIVATE = """
            UPDATE todos
            SET active = FALSE
            WHERE id = %(id)s;
        """

        DELETE = """
            DELETE FROM todos
            WHERE id = %(id)s;
        """

        CLEAN = """
            TRUNCATE TABLE todos;
        """

    @staticmethod
    def factory(max_connections: int = 10):
        connection_url = os.environ.get(
            "POSTGRESQL_CONNECTION_URL",
            "postgres://postgres:password@localhost:5432/postgres",
        )
        return PostgreSQLRepository(
            connection_url=connection_url, max_connections=max_connections
        )

    def __init__(self, connection_url: str, max_connections: int):
        self._connection_url = connection_url
        self._max_connections = max_connections
        self._pool: Optional[ThreadedConnectionPool] = None
        register_uuid()

    def connect(self) -> None:
        assert self._pool is None
        self._pool = ThreadedConnectionPool(
            minconn=1, maxconn=self._max_connections, dsn=self._connection_url
        )

    def disconnect(self) -> None:
        assert self._pool is not None
        self._pool.closeall()
        self._pool = None

    def initialize(self) -> None:
        with self._connection() as conn:
            with conn:
                with conn.cursor() as curs:
                    curs.execute(self.SQL.CREATE_UUID_EXTENSION)
                with conn.cursor() as curs:
                    curs.execute(self.SQL.CREATE_TABLE)

    def stats(self) -> Stats:
        data = {}

        with self._cursor() as curs:
            curs.execute(self.SQL.STATS)
            for row in curs:
                active = row[0]
                count = row[1]
                data[active] = count

        return Stats(active=data.get(True, 0), inactive=data.get(False, 0))

    def get(self, id_: UUID) -> Optional[Todo]:
        with self._cursor() as curs:
            curs.execute(self.SQL.GET, {"id": id_})
            row = curs.fetchone()
            if row is None:
                return None
            else:
                return Todo(id=id_, text=row[0], active=row[1])

    @rare_delay(delay=1.5, probability=0.2)
    def list(self) -> Tuple[Todo, ...]:
        todos = []

        with self._cursor() as curs:
            curs.execute(self.SQL.LIST)
            for row in curs:
                todo = Todo(id=row[0], text=row[1], active=row[2])
                todos.append(todo)

        return tuple(todos)

    @random_delay(min_delay=0.5, max_delay=2.0)
    def insert(self, text: str) -> UUID:
        with self._cursor() as curs:
            curs.execute(self.SQL.INSERT, {"text": text, "active": True})
            return curs.fetchone()[0]

    def edit_text(self, id_: UUID, text: str) -> bool:
        with self._cursor() as curs:
            curs.execute(self.SQL.EDIT_TEXT, {"id": id_, "text": text})
            return curs.rowcount > 0

    def activate(self, id_: UUID) -> bool:
        with self._cursor() as curs:
            curs.execute(self.SQL.ACTIVATE, {"id": id_, "active": True})
            return curs.rowcount > 0

    @rare_delay(delay=3.0, probability=0.1)
    def deactivate(self, id_: UUID) -> bool:
        with self._cursor() as curs:
            curs.execute(self.SQL.DEACTIVATE, {"id": id_, "active": False})
            return curs.rowcount > 0

    def delete(self, id_: UUID) -> bool:
        with self._cursor() as curs:
            curs.execute(self.SQL.DELETE, {"id": id_})
            return curs.rowcount > 0

    def _clean(self) -> None:
        with self._cursor() as curs:
            curs.execute(self.SQL.CLEAN)

    @contextmanager
    def _connection(self) -> ContextManager[connection]:
        assert self._pool is not None

        conn = self._pool.getconn()
        try:
            yield conn
        finally:
            self._pool.putconn(conn)

    @contextmanager
    def _cursor(self) -> ContextManager[cursor]:
        with self._connection() as conn:
            with conn:
                with conn.cursor() as curs:
                    yield curs
