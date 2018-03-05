import google
from firebase_admin import firestore

from firebase_orm.exeptions import DoesNotExist


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

        self._model._Model__autoincrement = False
        obj = self._model()
        self._model._Model__autoincrement = True

        obj._meta = {'id': pk}

        data = self._get_data(pk)
        # установка значений полей базы данных в model._meta
        for key in self._model_fields:
            obj._meta[key] = data.get(key)
        return obj

    def _id_autoincrement(self):
        docs = self._get_ref_col().order_by('id', direction=firestore.Query.DESCENDING).limit(1).get()
        for d in docs:
            pk = int(d.id) + 1
            return pk

    def _get_ref_col(self):
        db_table = self._model.Meta.db_table
        return self.db.collection(db_table)

    def _get_ref_doc(self, pk):
        doc_ref = self._get_ref_col().document(str(pk))
        return doc_ref

    def _get_data(self, pk):
        doc_ref = self._get_ref_doc(pk)
        try:
            doc = doc_ref.get()
            data = doc.to_dict()
        except google.cloud.exceptions.NotFound:
            raise DoesNotExist
        return data

    def _save(self, pk, meta):
        doc_ref = self._get_ref_doc(pk)
        doc_ref.update(meta, firestore.CreateIfMissingOption(True))
