import typing

import psycopg2
from psycopg2.extras import RealDictCursor

from Infrastructure.Database.IDatabase import IDatabase


class Database(IDatabase):

    def __init__(self, db: str, user: str, password: str, host: str, port: str):
        self.db = db
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        return psycopg2.connect(database=self.db, user=self.user, password=self.password, host=self.host,
                                port=self.port)

    def execute(self, sql: str, params: tuple = None, obj: typing.Callable = None):
        try:
            with self.connect() as connection:
                with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(sql, params)

                    if cursor.description is None:
                        return None

                    rows = cursor.fetchall()
                    if obj:
                        return [obj(**row) for row in rows]
                    return rows
        except psycopg2.Error as e:
            # TODO: actually log this instead of just printing to console
            print(f"Database error: {e}")
            raise
