from python_orm.mapper.StandardHolder import StandardHolder
from python_orm.objects.types import VarcharObject
from tests.utils import init_orm

class DumbObject(StandardHolder):
    @classmethod
    def register_class(cls):
        super().register_class()
        cls._register_object("dumby", VarcharObject("default"), primary=True)
        cls._register_object("ymbud", VarcharObject("ltuafed"))
        cls._define_properties()

DumbObject.register_class()

def test_dumb_object():
    obj = DumbObject()
    orm = init_orm()

    orm.get_connector().execute_query(f"describe {DumbObject.__name__}")
    obj.save()

    # equal
    obj_new = orm.get_mapper().get(DumbObject, limit=1)[0]
    assert obj_new.dumby == obj.dumby
    assert obj_new.ymbud == obj.ymbud
    assert obj_new == obj

    # not equal
    obj.dumby = "coucou"
    assert obj != obj_new

    obj_new.ymbud = "migouel"
    obj_new.save()
    obj = orm.get_mapper().get(DumbObject, limit=1)[0]
    assert obj_new.ymbud == obj.ymbud

    assert len(DumbObject.get(limit=1)) == 1
    obj_new.remove()
    assert len(DumbObject.get()) == 0