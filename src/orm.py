from src.mapper.ObjectMapper import ObjectMapper
from src.dao.MysqlConnector import ConnectorData, MysqlConnector

class ORM:
    """Self simple orm, this class is a singleton"""
    _instance = None

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)
        return cls._instance

    def init(self, config: ConnectorData):
        self._connector = MysqlConnector(config)
        self._mapper = ObjectMapper(self._connector)

    def get_mapper(self):
        return self._mapper
    
    def get_connector(self):
        return self._connector
