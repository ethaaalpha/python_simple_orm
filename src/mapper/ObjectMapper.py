from src.dao.MysqlConnector import MysqlConnector

class ObjectMapper():
    registered_class = []

    def __init__(self, connector):
        self._connector: MysqlConnector = connector

    def create_class_db(self):
        for holder in self.registered_class:
            self._connector.execute_update(holder.get_definition())

    def add_or_update(self, holder):
        names, values = self.__names_and_values(holder)
        query = self.__upsert_method(holder.table_name, names, values)

        self._connector.execute_update(query)

    def remove(self, holder):
        names, values = self.__names_and_values(holder)
        query = self.__delete_method(holder.table_name, names, values)

        self._connector.execute_update(query)

    def get(self, holder_class, primary_values):
        query = self.__get_method(holder_class.primary, primary_values)

        print(query)
        # self._connector.execute(query)

    def __names_and_values(self, holder):
        names = [name for name in holder._values.keys()]
        values = [f"{it.value_to_sqltype()}" for it in holder._values.values()]
        return names, values

    @staticmethod
    def __upsert_method(table_name, names, values):
        names_joined = ', '.join(names)
        values_joined  = ', '.join(values)

        update_part = ', '.join([f"{n}=VALUES({n})" for n in names])

        return f""" INSERT INTO {table_name} ({names_joined})
                    VALUES ({values_joined})
                    ON DUPLICATE KEY UPDATE {update_part};
                    """
    
    @staticmethod
    def __delete_method(table_name, names, values):
        mapped = dict(zip(names, values))
        mapped_joined = " AND ".join(f"{k}={v}" for k, v in mapped.items())

        return f"DELETE FROM {table_name} WHERE {mapped_joined};"
    
    @staticmethod
    def __get_method(table_name, names, values):
        mapped = dict(zip(names, values))
        mapped_joined = ", ".join(f"{k}={v}" for k, v in mapped.items())

        return f"SELECT * FROM {table_name} WHERE {mapped_joined};"
