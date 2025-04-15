from python_orm.objects.StandardObject import StandardObject

class IntegerObject(StandardObject):
    def __init__(self, value, size = 2147483647):
        self.is_type_of(value, int)
        super().__init__(value)

        self._size = size

    def get_sql(self):
        return f"int({self.size})"
