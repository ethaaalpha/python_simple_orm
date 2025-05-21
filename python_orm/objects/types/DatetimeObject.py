from python_orm.objects.StandardObject import StandardObject
from datetime import datetime

class DatetimeObject(StandardObject):
    format = "%Y-%m-%d %H:%M:%S"

    def __init__(self, value=datetime.now(), validator=None):
        self.is_type_of(value, datetime)
        super().__init__(value, validator)

    def get_sql(self):
        return f"DATETIME"

    def value_to_sqltype(self):
        return "'" + datetime.strftime(self._value, self.format) + "'"
    
    def sqltype_to_value(self, sql_value):
        return datetime.strptime(sql_value, self.format)
