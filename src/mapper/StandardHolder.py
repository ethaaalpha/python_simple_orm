from abc import ABC
from src.objects.StandardObject import StandardObject

class StandardHolder(ABC):
    def __init__(self, table_name: str):
        self.__properties: dict[str, StandardObject] = {}
        self.__table_name = table_name
        self.__primary = []

    def register_object(self, property_name: str, property_object: StandardObject, primary = False):
        if self.__properties.get(property_name) != None:
            raise NameError("Property name already existing")
        if len(property_name) == 0:
            raise NameError("Property musn't be empty")

        self.__properties[property_name] = property_object
        if primary:
            self.__primary.append(property_name)

        self.__define_property(property_name)

    def get_definition(self) -> str:
        query = f"CREATE TABLE IF NOT EXISTS {self.__table_name} ("
        query += ', '.join(f"{k} {prop.get_sql()} NOT NULL DEFAULT '{prop.value_to_str()}'" for k, prop in self.__properties.items())
        query += ", PRIMARY KEY (" 
        query += ', '.join(prim for prim in self.__primary)
        query += "));"

        return query

    def __define_property(self, property_name):
        """Create @property setter and getter for the property, use: self.property"""
        def getter(instance):
            return instance.__properties[property_name].value

        def setter(instance, property_value):
            instance.__properties[property_name].value = property_value

        setattr(self.__class__, property_name, property(getter, setter))
