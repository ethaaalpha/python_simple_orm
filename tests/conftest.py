import pytest
from python_orm.dao.MysqlConnector import MysqlConnector
from python_orm.orm import ORM

@pytest.fixture(autouse=True)
def reset_orm():
    ORM._instance = None 

@pytest.fixture(autouse=True)
def define_raise_sql():
    MysqlConnector.error = True