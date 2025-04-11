from abc import ABC, abstractmethod

class StandardObject(ABC):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def sqltype_to_value(self, sql_value):
        """Should be only used for dao operations"""
        return sql_value

    def value_to_sqltype(self):
        """Should be only used for dao operations"""
        return self.value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    @abstractmethod
    def get_sql(self):
        pass

    @staticmethod
    def is_type_of(value, type):
        if isinstance(value, type):
            return
        else:
            raise TypeError(f"Invalid type value should be {type}")
