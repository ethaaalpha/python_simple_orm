from dataclasses import dataclass, asdict
import mysql.connector as mysql 

@dataclass
class ConnectorData:
    host: str
    port: int
    username: str
    password: str
    database: str

class MysqlConnector:
    _instance = None
    
    # singleton
    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self, data: ConnectorData):
        self._data = data

    def connect(self):
        # see https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        if self.link == None or not self.link.is_connected():
            self.link = mysql.connect(**asdict(self._data))

    def disconnect(self):
        if self.link.is_connected():
            self.link.disconnect()

    def execute_query(self, query, params) -> list[tuple]:
        with self.link.cursor() as cursor:
            cursor.execute(query, params)

            result = cursor


    def execute_update(self, query, params):
        with self.link.cursor() as cursor:
            try:
                cursor.execute(query, params)
            except mysql.Error as err:
                print("Failed creating database: {}".format(err))
                exit(1)
