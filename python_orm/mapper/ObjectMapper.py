from python_orm.dao.MysqlConnector import MysqlConnector

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

    def remove_multiple(self, holder_class, comparators: list[str]):
        """We recommand to use `Comparators` methods."""

        query = self.__delete_multi_method(holder_class.table_name, comparators)

        self._connector.execute_update(query)

    def get(self, holder_class, comparators: list[str] = [], limit=None, order: list[str] = None) -> list:
        """We recommand to use `Comparators`, `Orders` methods."""
        selection = list(holder_class.properties.keys())
        extra_params = " "

        if (limit != None):
            extra_params += f"LIMIT {limit} "
        if (order != None):
            extra_params += "ORDER BY "
            extra_params += ", ".join(o for o in order)

        query = self.__get_method(holder_class.table_name, selection, comparators, extra_params)
        results = self._connector.execute_query(query)

        return self.__results_to_holders(selection, results, holder_class)

    def __results_to_holders(self, selection, results, result_class):
        zip_results = [dict(zip(selection, row)) for row in results]
        holders = []

        for row in zip_results:
            h = result_class()
            
            for attr, value in row.items():
                setattr(h, attr, value)
            holders.append(h)
        return holders

    def __names_and_values(self, holder):
        names = [name for name in holder._values.keys()]
        values = [f"{it.value_to_sqltype()}" for it in holder._values.values()]

        return names, values

    @staticmethod
    def __upsert_method(table_name, names, values):
        names_joined = ', '.join(names)
        values_joined  = ', '.join(values)

        update_part = ', '.join([f"{n}=VALUES({n})" for n in names])

        return f""" INSERT INTO `{table_name}` ({names_joined})
                    VALUES ({values_joined})
                    ON DUPLICATE KEY UPDATE {update_part};
                    """
    
    @staticmethod
    def __delete_method(table_name, names, values):
        mapped = dict(zip(names, values))
        mapped_joined = " AND ".join(f"{k}={v}" for k, v in mapped.items())

        return f"DELETE FROM `{table_name}` WHERE {mapped_joined};"
    
    @staticmethod
    def __get_method(table_name, selection: list, comparators: list, extra_params: str):
        comparators_joined = " AND ".join(comp for comp in comparators)
        selection_joined = ", ".join(item for item in selection)

        if (len(comparators) == 0):
            return f"SELECT {selection_joined} FROM `{table_name}`{extra_params};"
        else:
            return f"SELECT {selection_joined} FROM `{table_name}` WHERE {comparators_joined}{extra_params};"

    @staticmethod
    def __delete_multi_method(table_name, comparators: list):
        comparators_joined = " AND ".join(comp for comp in comparators)

        return f"DELETE FROM `{table_name}` WHERE {comparators_joined};"
