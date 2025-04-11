from abc import ABC
from src.objects.StandardObject import StandardObject

class StandardHolder(ABC):
    __properties: dict[str, StandardObject] = {}
    __table_name = None
    __primary = []

    def __new__(cls, table_name):
        cls.__table_name = table_name
        return super().__new__()

    @classmethod
    def register_object(cls, property_name: str, property_object: StandardObject, primary = False):
        if cls.__properties.get(property_name) != None:
            raise NameError("Property name already existing")
        if len(property_name) == 0:
            raise NameError("Property musn't be empty")

        cls.__properties[property_name] = property_object
        if primary:
            cls.__primary.append(property_name)

        cls.__define_property(property_name)

    @classmethod
    def get_definition(cls) -> str:
        query = f"CREATE TABLE IF NOT EXISTS `{cls.__table_name}` ("
        query += ', '.join(f"`{k}` {prop.get_sql()} NOT NULL DEFAULT '{prop.value_to_str()}'" for k, prop in cls.__properties.items())
        query += ", PRIMARY KEY (" 
        query += ', '.join(f"`{prim}`" for prim in cls.__primary)
        query += "));"

        return query

    @classmethod
    def __define_property(cls, property_name):
        """Create @property setter and getter for the property, use: self.property"""
        def getter(instance):
            return instance.__properties[property_name].value

        def setter(instance, property_value):
            instance.__properties[property_name].value = property_value

        setattr(cls.__class__, property_name, property(getter, setter))
