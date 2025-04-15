class Orders():
    @staticmethod
    def asc(col_name: str):
        return f"{col_name} ASC"

    def desc(col_name: str):
        return f"{col_name} DESC"