from python_orm.mapper.ObjectMapper import ObjectMapper
from python_orm.dao.MysqlConnector import ConnectorData, MysqlConnector

def ensure_initied(func):
    def wrapper(self, *args, **kwargs):
        if not self._initied:
            raise RuntimeError("ORM must be initied to do that!")
        return func(self, *args, **kwargs)
    return wrapper

class ORM:
    """Self simple orm, this class is a singleton"""
    _instance = None
    _initied = False

    def __new__(cls):
        if not isinstance(cls._instance, cls):
            cls._instance = super().__new__(cls)
        return cls._instance

    def init(self, config: ConnectorData):
        if not self._initied:
            self._connector = MysqlConnector(config)
            self._mapper = ObjectMapper(self._connector)
            self._mapper.create_class_db()
            self._initied = True
        else:
            raise RuntimeError("ORM can't be initied twice!")

    @ensure_initied
    def get_mapper(self):
        return self._mapper
    
    @ensure_initied
    def get_connector(self):
        return self._connector
