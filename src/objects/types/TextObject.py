from src.objects.StandardObject import StandardObject

class TextObject(StandardObject):
    """Max size is `16384`."""

    def __init__(self, value):
        super().__init__(value)

    def get_sql(self):
        return "text(16384)"

    def value_to_sqltype(self, value):
        return value
    
    def sqltype_to_value(self):
        return self._value