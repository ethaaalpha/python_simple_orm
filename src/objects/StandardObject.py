from abc import ABC, abstractmethod

class StandardObject(ABC):
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        self._value = new_value

    @abstractmethod
    def get_sql(self):
        pass

    @abstractmethod
    def value_to_sqltype(self, value):
        """Should be only used for dao operations"""
        pass

    @abstractmethod
    def sqltype_to_value(self):
        """Should be only used for dao operations"""
        pass
