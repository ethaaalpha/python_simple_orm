from dataclasses import dataclass, asdict
import mysql.connector as mysql

from src.utils.decorators import singleton 

@dataclass
class ConnectorData:
    host: str
    port: int
    username: str
    password: str
    database: str

@singleton
class MysqlConnector:
    def __init__(self, data: ConnectorData):
        self.link = None
        self._data = data

    def connect(self):
        # see https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        if self.link == None or not self.link.is_connected():
            self.link = mysql.connect(**asdict(self._data))

    def disconnect(self):
        if self.link.is_connected():
            self.link.disconnect()

    @classmethod
    def execute_query(cls, query, params) -> list[tuple]:
        connector = MysqlConnector()
        connector.connect()

        with connector.link.cursor() as cursor:
            cursor.execute(query, params)

            result = cursor
        connector.disconnect()

    @classmethod
    def execute_update(cls, query, params):
        connector = MysqlConnector()
        connector.connect()

        print(connector.link.cursor(connector))
        with connector.link.cursor() as cursor:
            try:
                cursor.execute(query, params)
            except mysql.Error as err:
                print("Failed creating database: {}".format(err))
        connector.disconnect()
