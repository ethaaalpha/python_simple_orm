from python_orm.objects.StandardObject import StandardObject

class IntegerObject(StandardObject):
    def __init__(self, value, size = 255, validator=None):
        self.is_type_of(value, int)
        super().__init__(value, validator)

        self._size = size

    def get_sql(self):
        return f"int({self._size})"

    
    def sqltype_to_value(self, sql_value):
        return int(sql_value)