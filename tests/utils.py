from python_orm.orm import ORM
from python_orm.dao.MysqlConnector import ConnectorData

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
    return orm
