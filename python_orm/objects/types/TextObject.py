from python_orm.objects.StandardObject import StandardObject

class TextObject(StandardObject):
    def __init__(self, size = 16384):
        super().__init__(None)

        if size <= 0:
            raise ValueError("Size must be > 0!")
        else:
            self._size = size

    def get_sql(self):
        return f"text({self._size})"
