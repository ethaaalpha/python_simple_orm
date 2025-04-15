from python_orm.objects.StandardObject import StandardObject

class FloatObject(StandardObject):
    def __init__(self, value, precision = 15):
        self.is_type_of(value, float)
        super().__init__(value)

        if precision <= 0:
            raise ValueError("Size must be > 0!")
        else:
            self._size = precision

    def get_sql(self):
        return f"float({self.precision})"
