from python_orm.objects.StandardObject import StandardObject
from datetime import datetime

class DatetimeObject(StandardObject):
    def __init__(self, value):
        self.is_type_of(value, datetime)
        super().__init__(value)

    def get_sql(self):
        return f"DATETIME({self.precision})"

    def value_to_sqltype(self):
        return None
        # return datetime.strftime()
    
    def sqltype_to_value(self, sql_value):
        return None
        # return datetime.strptime(value,)
