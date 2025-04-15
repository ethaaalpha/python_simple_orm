from python_orm.objects.StandardObject import StandardObject

class BooleanObject(StandardObject):
    def __init__(self, value):
        self.is_type_of(value, bool)
        super().__init__(value)

    def get_sql(self):
        return f"boolean"

    def value_to_sqltype(self):
        return str(self._value)
    
    def sqltype_to_value(self, sql_value):
        if sql_value.lower() in ("true", "1", "yes"):
            return True
        elif sql_value.lower() in ("false", 0, "no"):
            return False