from firebase_orm.exeptions import CanNotBeChanged


class Field:
    def __init__(self, db_column=None):
        self.db_column = db_column

    def __get__(self, obj, objtype):
        return obj._meta.get(self.db_column)

    def __set__(self, obj, val):
        if val is None:
            obj._meta[self.db_column] = val
        elif not str(val).strip():
            obj._meta[self.db_column] = None


class TextString(Field):
    pass


class IDField:
    def __init__(self):
        self.db_column = 'id'

    def __get__(self, obj, objtype):
        return obj._meta.get(self.db_column)

    def __set__(self, obj, val):
        raise CanNotBeChanged


