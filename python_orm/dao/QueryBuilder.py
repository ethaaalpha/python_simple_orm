from typing import Iterable
from python_orm.dao.operators.Comparators import ComparatorData

class Query:
    def __init__(self, starter):
        self._members = [starter]
        self._params = []
        self._where = False
        self._order = False

    def add_member(self, member):
        self._members.append(member)
    
    def add_param(self, param):
        if isinstance(param, Iterable):
            for item in param:
                self._params.append(item)
        else:
            self._params.append(param)

    def add_where(self, comparator: ComparatorData):
        if self._where:
            self.add_member("AND")
        else:
            self.add_member("WHERE")
            self._where = True

        self._members.append(f"{comparator.left}{comparator.sign}%s")
        self._params.append(comparator.right)

    def add_order(self, order):
        if self._order:
            self.add_member(", ")
        else:
            self.add_member("ORDER BY")
            self._order = True

        self._members.append(order)

    def get_sql(self, limit=None) -> str:
        if limit:
            self.add_member(f"LIMIT {limit}")
        return " ".join(self._members)

    def get_params(self) -> list:
        return self._params

    @classmethod
    def upsert(cls,table_name: str, columns: list[str], values: list):
        query = Query(f"INSERT INTO `{table_name}`")
        placeholders_insert = ', '.join(['%s'] * len(values))
        placeholders_duplicate = ', '.join(f"{col} = %s" for col in columns)

        query.add_member(f"({columns_as_string(columns)})")
        query.add_member("VALUES")
        query.add_member(f"({placeholders_insert})")
        query.add_param(values)

        query.add_member("ON DUPLICATE KEY UPDATE")
        query.add_member(f"{placeholders_duplicate}")
        query.add_param(values)

        return query

    @classmethod
    def select(cls, table_name: str, columns: list[str]):
        return Query(f"SELECT {columns_as_string(columns)} FROM `{table_name}`")
    
    @classmethod
    def delete(cls, table_name: str):
        return Query(f"DELETE FROM `{table_name}`")
    
    @classmethod
    def truncate(cls, table_name: str):
        return Query(f"TRUNCATE TABLE `{table_name}`")
    
def columns_as_string(columns: list[str]):
    return ", ".join(columns)