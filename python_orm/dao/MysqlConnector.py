from dataclasses import dataclass, asdict
from pprint import pprint
import mysql.connector as mysql
import sys

@dataclass
class ConnectorData:
    host: str
    port: int
    username: str
    password: str
    database: str

class MysqlConnector:
    error = False

    def __init__(self, data: ConnectorData):
        self.link = None
        self._data = data

    def connect(self):
        # see https://dev.mysql.com/doc/connector-python/en/connector-python-connectargs.html
        if self.link == None or not self.link.is_connected():
            self.link = mysql.connect(**asdict(self._data))
            self.link.autocommit = True

    def disconnect(self):
        if self.link.is_connected():
            self.link.disconnect()

    def execute_update(self, query, params = {}):
        self.connect()
        
        print(f"update query: {query}")
        with self.link.cursor() as cursor:
            try:
                cursor.execute(query, params)
            except mysql.Error as err:
                if self.error:
                    raise err
                print("Failed running update query: {}".format(err), file=sys.stderr)
        self.disconnect()

    def execute_query(self, query, params = {}):
        self.connect()

        print(f"select query: {query}")
        with self.link.cursor() as cursor:
            try:
                cursor.execute(query, params)
                return cursor.fetchall()
            except mysql.Error as err:
                if self.error:
                    raise err
                print("Failed running fetch query: {}".format(err), file=sys.stderr)     
        self.disconnect()
