from src.objects.types.VarcharObject import VarcharObject
from src.dao.MysqlConnector import ConnectorData, MysqlConnector
from src.mapper.ObjectMapper import ObjectMapper
from src.mapper.StandardHolder import StandardHolder
from src.objects.types.TextObject import TextObject
from src.dao.operators.Comparators import Comparators as Cp
from src.dao.operators.Orders import Orders as Or

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
# mysql --host=127.0.0.1 --user=root --password=my-secret-pw test
# docker run --rm --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=test -p 3306:3306 -d mysql:latest

connect = MysqlConnector(data)
User.register_class()

default = User()
dumb = User()
dumb.prename = "Migouelito"
dumb.name = "jdpiwajdiw"
dumb.proname = "djwpiadwijp"

ObjectMapper(connect).create_class_db()
ObjectMapper(connect).add_or_update(default)
ObjectMapper(connect).add_or_update(dumb)
result = ObjectMapper(connect).get(User)[0]

print(result.name)
print(result.proname)
print(result.prename)


# ObjectMapper(connect).add_or_update(User())
# import time
# time.sleep(30)
# ObjectMapper(connect).remove(User())

# StandardHolder._register_object("name", TextObject("migouel"), primary=True)
# StandardHolder._register_object("proname", TextObject(""), primary=True)
# StandardHolder._register_object("prename", TextObject("alfred"), primary=True)
# holder = StandardHolder()

# print(holder.prename)
# holder.prename = "5"
# print(holder.prename)

# holderBis = StandardHolder()
# print(holderBis.prename)
# holderBis.prename = "1"
# print(holderBis.prename)

# holderBisBis = StandardHolder()
# print(holderBisBis.prename)
# holderBisBis.prename = "dwqdwqdw"
# print(holderBisBis.prename)
