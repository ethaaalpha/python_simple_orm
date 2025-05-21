from python_orm.objects.StandardObject import StandardObject

class VarcharObject(StandardObject):
    def __init__(self, value, size=255, validator=None):
        self.is_type_of(value, str)
        super().__init__(value, validator)

        if size <= 0:
            raise ValueError("Size must be > 0!")
        else:
            self._size = size

    def get_sql(self):
        return f"varchar({self._size})"
