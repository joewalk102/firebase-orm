from firebase_orm.models.manager import Manager
from firebase_orm.models.fields import Field, IDField


class ModelBase(type):
    """Metaclass for all models."""
    def __new__(cls, name, bases, attrs):
        super_new = super().__new__
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)
        """
        _meta содержит данные:
            значения полей в базе данных для дескрипторов
            ключем является именно название поля базы данных, а не имя переменной дескриптора
        """
        attrs['_meta'] = {}

        attrs['objects'] = Manager()
        attrs['id'] = IDField()
        return super_new(cls, name, bases, attrs)

    def __init__(self, name, bases, attrs):
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            return

        # добавление класса модели в менеджер
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

    def __init__(self, **kwargs):
        """все объекты и данные экземпляра хранятся в словаре self._meta"""
        """
        инициализация полей модели Manager
        ключи - названия полей в базе данных
        значения - название полей модели
        """
        attrs = self.__dict__
        for key in attrs:
            val = attrs[key]
            if issubclass(type(val), Field):
                self.objects._model_fields[val.__dict__.get('db_column')] = key

        """инициализация происходит в двух случаях
        1. Создание `Model(name='any name')`
            id устанавливается из автоинкремента менеджера
            наполняет self._meta значениями полей, если переданы параметры в kwargs
        2. Наполнение из базы данных `Model.object.get(id='1')`
            наполнение self._meta передается Manager
        """
        if not self._meta.pop('__no_autoincrement', False):
            self._meta['id'] = self.objects._id_autoincrement()

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
