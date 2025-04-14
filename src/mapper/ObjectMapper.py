from src.dao.MysqlConnector import MysqlConnector

class ObjectMapper():
    registered_class = []

    def create_class_db(self):
        for holder in self.registered_class:
            MysqlConnector().execute_update(holder.get_definition(), {})
