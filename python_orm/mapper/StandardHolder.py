from abc import ABC, abstractmethod
from python_orm.orm import ORM
from python_orm.mapper.ObjectMapper import ObjectMapper
from python_orm.objects.StandardObject import StandardObject
import copy

class StandardHolder(ABC):
    """StandardHolder is a simple mapped to database object, we recomm end of the definition class file."""
    primary = []
    table_name = None
    properties: dict[str, tuple[type[StandardObject], dict]] = {}

    def __init__(self):
        self._values = copy.deepcopy(self.properties)

    def save(self):
        ORM().get_mapper().add_or_update(self)

    def remove(self):
        ORM().get_mapper().remove(self)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if len(self.properties) == len(other.properties) and self.properties.keys() == other.properties.keys():
                for property in self.properties.keys():
                    if getattr(other, property) != getattr(self, property):
                        return False
                return True
            else:
                return False
        return False

    @classmethod
    def get(cls, **kwargs) -> list:
        """See `ObjectMapper.get()` for kwargs."""
        return ORM().get_mapper().get(cls, **kwargs)

    @classmethod
    def get_definition(cls) -> str:
        query = f"CREATE TABLE IF NOT EXISTS `{cls.table_name}` ("
        query += ', '.join(f"`{k}` {prop.get_sql()} \
{"NOT NULL DEFAULT " + prop.value_to_sqltype() if not prop.no_default else "NULL"}" for k, prop in cls.properties.items())
        query += ", PRIMARY KEY (" 
        query += ', '.join(f"`{prim}`" for prim in cls.primary)
        query += "));"

        return query

    @classmethod
    @abstractmethod
    def register_class(cls):
        """
        This method should be run ONCE.
        You should use at least `_register_table_name`, `_define_properties` and between them
        `_register_object`.  
        The super() method should be called at the BEGENING of the function.
        """
        cls.properties = {}
        cls.table_name = cls.__name__
        cls.primary = []

        if cls not in ObjectMapper.registered_class:
            ObjectMapper.registered_class.append(cls) 

    @classmethod
    def _register_object(cls, property_name: str, property_object: type[StandardObject], primary = False):
        """Should be use in `register_class()` method."""
        if cls.properties.get(property_name) != None:
            raise NameError("Property name already existing")
        if len(property_name) == 0:
            raise NameError("Property musn't be empty")

        cls.properties[property_name] = property_object
        if primary:
            cls.primary.append(property_name)

    @classmethod
    def _register_table_name(cls, table_name: str):
        cls.table_name = table_name

    @classmethod
    def _define_properties(cls):
        """Create @property setter and getter for each class properties, use: self.property"""
        for property_name in cls.properties.keys():
            def getter(instance, name=property_name):
                return instance._values[name].value

            def setter(instance, property_value, name=property_name):
                instance._values[name].value = property_value

            setattr(cls, property_name, property(getter, setter))
