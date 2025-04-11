from src.objects.StandardObject import StandardObject

class BooleanObject(StandardObject):
    def __init__(self, value):
        self.is_type_of(value, bool)
        super().__init__(value)

    def get_sql(self):
        return f"boolean"
