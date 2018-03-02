from firebase_orm.models.manager import Manager
from firebase_orm.models.fields import Field, IDField


class ModelBase(type):
    """Metaclass for all models."""
    def __new__(cls, name, bases, attrs):
        super_new = super().__new__
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        attrs['_meta'] = {}
        attrs['objects'] = Manager()
        attrs['id'] = IDField()
        return super_new(cls, name, bases, attrs)

    def __init__(self, name, bases, attrs):
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            return

        # добавление модели в менеджер
        manager = attrs['objects']
        manager._model = self

        # установка дескрипторам полей имени колонки в базе данных
        for key in attrs:
            data = attrs[key]
            if issubclass(type(data), Field) and not attrs.get(key).db_column:
                setattr(data, 'db_column', key)
        type.__init__(self, name, bases, attrs)


class Model(metaclass=ModelBase):
    objects = Manager()

    def __init__(self):
        if not self._meta.pop('__get', False):
            id = self.objects._id_autoincrement()
            self._meta['id'] = id

    def __eq__(self, other):
        keys = self.objects._model_fields.values()
        fields = self._meta
        for key in keys:
            if not fields.get(key):
                fields[key] = None
        return fields == other._meta

    def save(self):
        self.objects._save(self.id, self._meta)

    def __repr__(self):
        return f'<{type(self).__name__}: {self.__str__()}>'
