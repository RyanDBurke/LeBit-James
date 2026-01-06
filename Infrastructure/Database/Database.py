import psycopg2

from Infrastructure.Database.IDatabase import IDatabase


class Database(IDatabase):
    def __init__(self, db: str, user: str, password: str, host: str, port: str):
        self.db = db
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        return psycopg2.connect(database=self.db, user=self.user, password=self.password, host=self.host, port=self.port)

    def execute(self, sql: str):
        # TODO: Validate

        connection = self.connect()

        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()

            connection.commit()
            cursor.close()
            connection.close()

            return result
        except psycopg2.Error as e:
            print(e)

        connection.commit()
        cursor.close()
        connection.close()
        return None

    def close(self):
        self.connection.close()

