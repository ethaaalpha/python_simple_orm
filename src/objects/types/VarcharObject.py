from src.objects.StandardObject import StandardObject

class VarcharObject(StandardObject):
    def __init__(self, value, size=1024):
        self.is_type_of(value, str)
        super().__init__(value)

        if size <= 0:
            raise ValueError("Size must be > 0!")
        else:
            self._size = size

    def get_sql(self):
        return f"varchar({self._size})"
