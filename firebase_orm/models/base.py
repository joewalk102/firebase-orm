from firebase_orm.models.manager import Manager
from firebase_orm.models.fields import Field, IDField


class ModelBase(type):
    """Metaclass for all models."""
    def __new__(cls, name, bases, attrs):
        super_new = super().__new__
        parents = [b for b in bases if isinstance(b, ModelBase)]
        if not parents:
            return super_new(cls, name, bases, attrs)

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
    __autoincrement = True

    def __init__(self, **kwargs):
        self._meta = {}
        """все объекты и данные экземпляра хранятся в словаре self._meta"""
        """
        инициализация полей модели Manager
        ключи - названия полей в базе данных
        значения - название полей модели
        """
        attrs = self.__class__.__dict__
        for key in attrs:
            val = attrs[key]
            if issubclass(type(val), Field):
                self.objects._model_fields[val.__dict__.get('db_column')] = key

        """инициализация происходит в двух случаях
        1. Создание `Model(name='any name')`
            - id устанавливается из автоинкремента менеджера
            - наполняет self._meta значениями полей, если переданы параметры в kwargs
        2. Установка атрибутов из базы данных `Model.object.get(id='1')`
            добавление атрибутов в self._meta происходит в Manager
        """
        if self._Model__autoincrement:
            # id в self._meta
            pk = self.objects._id_autoincrement()
            if not pk:
                pk = 0
            self._meta['id'] = pk
            # kwargs в self._meta
            for key, value in self.objects._model_fields.items():
                self._meta[key] = kwargs.get(value)

    def __eq__(self, other):
        if self._meta == other._meta:
            return True

    def save(self):
        self.objects._save(self.id, self._meta)

    def __repr__(self):
        return f'<{type(self).__name__}: {self.__str__()}>'
