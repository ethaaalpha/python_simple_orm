from python_orm.dao.MysqlConnector import MysqlConnector
from python_orm.dao.QueryBuilder import Query
from python_orm.dao.operators.Comparators import ComparatorData

class ObjectMapper():
    registered_class = []

    def __init__(self, connector):
        self._connector: MysqlConnector = connector

    def create_class_db(self):
        for holder in self.registered_class:
            self._connector.execute_update(holder.get_definition())

    def add_or_update(self, holder):
        columns, values = self._columns_and_values(holder)
        query = Query.upsert(holder.table_name, columns, values)

        self._connector.execute_update(query.get_sql(), query.get_params())

    def remove(self, holder, comparators: list[ComparatorData] = []):
        query = Query.delete(holder.table_name)

        for c in comparators:
            query.add_where(c)

        self._connector.execute_update(query.get_sql(), query.get_params())

    def get(self, holder_class, comparators: list[ComparatorData] = [], order: list[str] = [], limit=None) -> list:
        """We recommand to use `Comparators`, `Orders` methods."""
        columns = list(holder_class.properties.keys())
        query = Query.select(holder_class.table_name, columns)

        for c in comparators:
            query.add_where(c)
        for o in order:
            query.add_order(o)

        results = self._connector.execute_query(query.get_sql(), query.get_params())

        return self._results_to_holders(columns, results, holder_class)

    def clear_tables(self):
        for cls in self.registered_class:
            query = Query.truncate(cls.table_name)
            self._connector.execute_query(query.get_sql())

    def _results_to_holders(self, selection, results, result_class):
        zip_results = [dict(zip(selection, row)) for row in results]
        holders = []

        for row in zip_results:
            h = result_class()
            
            for attr, value in row.items():
                setattr(h, attr, value)
            holders.append(h)
        return holders

    def _columns_and_values(self, holder, only_primary=False):
        columns = holder.primary if only_primary else list(holder._values.keys())
        values = [holder._values[it].value_to_sqltype() for it in columns]

        return columns, values
