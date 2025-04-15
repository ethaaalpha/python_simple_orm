from python_orm.objects.types.VarcharObject import VarcharObject
from python_orm.dao.MysqlConnector import ConnectorData, MysqlConnector
from python_orm.mapper.ObjectMapper import ObjectMapper
from python_orm.mapper.StandardHolder import StandardHolder
from python_orm.objects.types.TextObject import TextObject
from python_orm.dao.operators.Comparators import Comparators as Cp
from python_orm.dao.operators.Orders import Orders as Or
from python_orm.orm import ORM

class User(StandardHolder):
    @classmethod
    def register_class(cls):
        super().register_class()
        cls._register_table_name("Usertesteu")
        cls._register_object("name", VarcharObject("migouel"), primary=True)
        cls._register_object("proname", VarcharObject("test"))
        cls._register_object("prename", VarcharObject("alfred"))
        cls._define_properties()

class UserBis(StandardHolder):
    def __init__(self):
        super().__init__()

    @classmethod
    def register_class(cls):
        super().register_class()
        cls._register_object("proname", VarcharObject(""), primary=True)
        cls._define_properties()

data = ConnectorData(
    host = "localhost",
    port = 3306,
    username="root",
    password="my-secret-pw",
    database="test"
)

orm = ORM()
orm.init(data)

mapper = orm.get_mapper()

User.register_class()
UserBis.register_class()

default = User()
dumb = User()
dumb.prename = "Migouelito"
dumb.name = "jdpiwajdiw"
dumb.proname = "djwpiadwijp"

default.save()
dumb.remove()
result = mapper.get(User)[0]

print(result.name)
print(result.proname)
print(result.prename)

# mysql --host=127.0.0.1 --user=root --password=my-secret-pw test
# docker run --rm --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=test -p 3306:3306 -d mysql:latest
# docker stop $(docker ps -q | tail -n 1)
