from python_orm.orm import ORM
from python_orm.dao.MysqlConnector import ConnectorData

# docker run --rm --name some-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -e MYSQL_DATABASE=test -p 3306:3306 -d mysql:latest
def init_orm() -> ORM:
    data = ConnectorData(
        host = "localhost",
        port = 3306,
        username="root",
        password="my-secret-pw",
        database="test"
    )

    orm = ORM()
    orm.init(data)
    orm.get_mapper().clear_tables()
    return orm
