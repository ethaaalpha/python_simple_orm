from tests.utils import init_orm

def test_connection_check():
    orm = init_orm()

    orm.get_connector().execute_query("SHOW TABLES;")
