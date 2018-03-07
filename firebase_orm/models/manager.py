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
        pk = kwargs.get('id')
        if not pk and pk is not 0:
            raise TypeError
        if type(pk) is not int:
            raise TypeError

        document = self._get_data(pk)

        return self._doc_to_instance(document)

    def all(self):
        documents = []
        count = 0
        count_list = -1
        while True:
            docs = self._get_ref_col().offset(count).limit(10).get()
            for doc in docs:
                documents.append(doc.to_dict())
                count += 1

            if len(documents) == count_list:
                break
            count_list = len(documents)
        instances = []
        for document in documents:
            instances.append(self._doc_to_instance(document))
        return instances

    def _doc_to_instance(self, document):
        self._model._Model__autoincrement = False
        obj = self._model()
        self._model._Model__autoincrement = True

        obj._meta = {'id': document['id']}
        # установка значений полей базы данных в model._meta
        for key in self._model_fields:
            obj._meta[key] = document.get(key)
        return obj

    def _id_autoincrement(self):
        def get_fast_id():
            docs = self._get_ref_col().order_by(
                'id',
                direction=firestore.Query.DESCENDING
            ).limit(1).get()
            for d in docs:
                return int(d.id)
        db_pk = get_fast_id()
        return db_pk+1 if db_pk or db_pk is 0 else 0

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
