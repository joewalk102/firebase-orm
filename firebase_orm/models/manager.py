import google
from firebase_admin import firestore

from firebase_orm.exeptions import DoesNotExist
from firebase_orm.models.fields import Field


class Manager:
    db = None
    bucket = None

    def __init__(self):
        self._model_fields = {}
        self._model = None

    def get(self, **kwargs):
        """
        :return: Model
        :raise: ObjectDoesNotExist
        """
        if not kwargs.get('id'):
            raise TypeError
        pk = kwargs.get('id')
        if type(pk) is not int:
            raise TypeError

        if not self._model_fields:
            self._dict_db_column()

        data = self._get_data(pk)

        self._model._meta['__get'] = True
        obj = self._model()
        obj._meta = {'id': pk}

        # установка значений полей базы данных в model._meta
        fields = self._model_fields
        for key in fields:
            field_key = fields.get(key)
            val = data.get(key)
            obj._meta[field_key] = val

        return obj

    def _dict_db_column(self):
        """
        установка полей модели в self._model_fields
        ключи - названия полей в базе данных
        значения - название полей модели
        :return: dict
        :rtype: dict
        """
        attrs = self._model.__dict__
        for key in attrs:
            val = attrs[key]
            if issubclass(type(val), Field):
                self._model_fields[val.__dict__.get('db_column')] = key

    def _id_autoincrement(self):
        doc_ref = self.db.collection('test')
        doc = doc_ref.order_by('id', direction=firestore.Query.DESCENDING).limit(1).get()
        for d in doc:
            id = int(d.id) + 1
            return id

    def _get_ref(self, pk):
        db_table = self._model.Meta.db_table
        doc_ref = self.db.collection(db_table).document(str(pk))
        return doc_ref

    def _get_data(self, pk):
        doc_ref = self._get_ref(pk)

        try:
            doc = doc_ref.get()
            data = doc.to_dict()
        except google.cloud.exceptions.NotFound:
            raise DoesNotExist
        return data

    def _save(self, pk, meta):
        doc_ref = self._get_ref(pk)
        doc_ref.update(meta, firestore.CreateIfMissingOption(True))
