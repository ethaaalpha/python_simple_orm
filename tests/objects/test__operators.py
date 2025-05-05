from datetime import datetime
from python_orm.dao.operators import *
from python_orm.objects.types import *
from python_orm.mapper.StandardHolder import StandardHolder
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

    @staticmethod
    def test_items():
        obj_a = AllHolder()
        obj_a.a_varchar = "caillou"
        obj_a.a_text = "text_coucou"
        obj_a.a_integer = 10
        obj_a.a_float = 10.12
        obj_a.a_datetime = datetime(2000, 1, 1)
        obj_a.a_boolean = True
        obj_a.save()
    
        obj_b = AllHolder()
        obj_b.a_varchar = "uolliac"
        obj_b.a_text = "text_salut"
        obj_b.a_integer = 11
        obj_b.a_float = 10.13
        obj_b.a_datetime = datetime(2000, 1, 2)
        obj_b.a_boolean = True
        obj_b.save()
    
        obj_c = AllHolder()
        obj_c.a_varchar = "abcdef"
        obj_c.a_text = "text_bonjour"
        obj_c.a_integer = 10
        obj_c.a_float = 10.14
        obj_c.a_datetime = datetime(2000, 1, 3)
        obj_c.a_boolean = False
        obj_c.save()

        return obj_a, obj_b, obj_c

def test_order():
    AllHolder.register_class()
    init_orm()

    obj = AllHolder()
    obj.save()

    assert len(AllHolder().get()) == 1

    obj.remove()
    assert len(AllHolder().get()) == 0

    obj = AllHolder()
    obj.a_varchar = "migouel"
    obj.save()

    obj_bis = AllHolder()
    obj_bis.a_varchar = "bigouel"
    obj_bis.save()

    assert AllHolder.get(order = [asc("a_varchar")])[0].a_varchar == "bigouel"
    assert AllHolder.get(order = [desc("a_varchar")])[1].a_varchar == "bigouel"

def test_comparators():
    AllHolder.register_class()
    init_orm()

    obj_a, obj_b, obj_c = AllHolder.test_items()

    def _eq():
        res = AllHolder.get(comparators = [eq("a_varchar", "caillou")])
        assert len(res) == 1 and obj_a in res

        res = AllHolder.get(comparators = [eq("a_text", "text_salut")])
        assert len(res) == 1 and obj_b in res

        res = AllHolder.get(comparators = [eq("a_integer", 10)])
        assert len(res) == 2 and obj_a, obj_c in res

        res = AllHolder.get(comparators = [eq("a_datetime", datetime(2000, 1, 2))])
        assert len(res) == 1 and obj_b in res

        res = AllHolder.get(comparators = [eq("a_boolean", False)])
        assert len(res) == 1 and obj_c in res

        res = AllHolder.get(comparators = [eq("a_integer", -12)])
        assert len(res) == 0

    def _gt():
        res = AllHolder.get(comparators = [gt("a_varchar", "caillou")])
        assert len(res) == 1 and obj_b in res

        res = AllHolder.get(comparators = [gt("a_text", "text_bonjour")])
        assert len(res) == 2 and obj_a, obj_a in res

        res = AllHolder.get(comparators = [gt("a_integer", 10)])
        assert len(res) == 1 and obj_b in res

        res = AllHolder.get(comparators = [gt("a_float", 10.131)])
        assert len(res) == 1 and obj_c in res

        res = AllHolder.get(comparators = [gt("a_datetime", datetime(2000, 1, 2))])
        assert len(res) == 1 and obj_c in res

        res = AllHolder.get(comparators = [gt("a_boolean", False)])
        assert len(res) == 2 and obj_a, obj_b in res

    def _lt():
        res = AllHolder.get(comparators = [lt("a_varchar", "caillou")])
        assert len(res) == 1 and obj_c in res

        res = AllHolder.get(comparators = [lt("a_text", "text_coucou")])
        assert len(res) == 1 and obj_c in res

        res = AllHolder.get(comparators = [lt("a_integer", 11)])
        assert len(res) == 2 and obj_a, obj_c in res

        res = AllHolder.get(comparators = [lt("a_float", 10.13)])
        assert len(res) == 1 and obj_a in res

        res = AllHolder.get(comparators = [lt("a_datetime", datetime(2000, 1, 3))])
        assert len(res) == 2 and obj_a, obj_b in res

        res = AllHolder.get(comparators = [lt("a_boolean", True)])
        assert len(res) == 1 and obj_c in res

    def _noteq():
        res = AllHolder.get(comparators = [noteq("a_varchar", "caillou")])
        assert len(res) == 2 and obj_b, obj_c in res

        res = AllHolder.get(comparators = [noteq("a_text", "text_coucou")])
        assert len(res) == 2 and obj_b, obj_c in res

        res = AllHolder.get(comparators = [noteq("a_integer", 11)])
        assert len(res) == 2 and obj_a, obj_c in res

        res = AllHolder.get(comparators = [noteq("a_datetime", datetime(2000, 1, 1))])
        assert len(res) == 2 and obj_b, obj_c in res

        res = AllHolder.get(comparators = [noteq("a_boolean", True)])
        assert len(res) == 1 and obj_c in res

    _eq()
    _gt()
    _lt()
    _noteq()

    res = AllHolder().get(comparators = [lt("a_integer", 11), gt("a_datetime", datetime(2000, 1, 1))])
    assert len(res) == 1 and obj_c in res

def test_comparators_orders():
    AllHolder.register_class()
    init_orm()

    obj_a, obj_b, _ = AllHolder.test_items()

    res = AllHolder.get(comparators = [eq("a_boolean", True)], order = [desc("a_datetime")])
    assert len(res) == 2 and res[0] == obj_b

    res = AllHolder.get(comparators = [lt("a_integer", 11)], order = [asc("a_float")])
    assert len(res) == 2 and res[0] == obj_a

    res = AllHolder.get(comparators = [lt("a_integer", 11)], order = [desc("a_text")])
    assert len(res) == 2 and res[0] == obj_a
