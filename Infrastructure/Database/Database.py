import psycopg2

from Infrastructure.Database.IDatabase import IDatabase


class Database(IDatabase):
    def __init__(self, db: str, user: str, password: str, host: str, port: str):
        self.db = db
        self.user = user
        self.password = password
        self.host = host
        self.port = port

        self.connection = self.connect()

    def connect(self):
        return psycopg2.connect(database=self.db, user=self.user, password=self.password, host=self.host, port=self.port)

    def query(self, sql: str):
        # TODO: Validate that this is a query

        cursor = self.connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
            return result
        except psycopg2.Error as e:
            print(e)

        cursor.close()
        return None

    def upsert(self, sql: str):
        # TODO: Validate that this is an update/insert

        cursor = self.connection.cursor()
        cursor.execute(sql)
        cursor.close()

    def close(self):
        self.connection.close()

