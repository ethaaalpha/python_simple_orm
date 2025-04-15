from datetime import datetime
from python_orm.mapper.StandardHolder import StandardHolder
from python_orm.objects.types import *
from tests.utils import init_orm

class AllHolder(StandardHolder):
    @classmethod
    def register_class(cls):
        super().register_class()
        cls._register_object("a_varchar", VarcharObject("default"), primary=True)
        cls._register_object("a_text", TextObject())
        cls._register_object("a_integer", IntegerObject(42))
        cls._register_object("a_float", FloatObject(42.42))
        cls._register_object("a_datetime", DatetimeObject(datetime.now()))
        cls._register_object("a_boolean", BooleanObject(False))
        cls._define_properties()

def test_complex():
    AllHolder.register_class()
    orm = init_orm()

    obj = AllHolder()
    obj.save()
    obj.remove()
    
    assert len(AllHolder().get()) == 0