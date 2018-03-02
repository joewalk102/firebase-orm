import pytest

from firebase_orm.models import Manager


@pytest.fixture(scope='session')
def db():
    d_b = Manager.db
    try:
        yield d_b
    finally:
        ids = []
        count_list = -1
        while True:
            docs = d_b.collection('test').limit(4).get()
            for doc in docs:
                ids.append(doc.id)
                doc.reference.delete()

            if len(ids) == count_list:
                break
            count_list = len(ids)
        del ids


@pytest.fixture(scope='session')
def del_all(db):
    ids = []
    count_list = -1
    while True:
        docs = db.collection('test').limit(4).get()
        for doc in docs:
            ids.append(doc.id)
            doc.reference.delete()

        if len(ids) == count_list:
            break
        count_list = len(ids)
    del ids


@pytest.fixture
def add_document(db):
    def add_data(id, name=None, type_test=None, author=None, brief=None):
        doc_ref = db.collection('test').document(id)
        doc_ref.set({
            'id': int(id),
            'name': name,
            'type_test': type_test,
            'author': author,
            'brief': brief
        })
    return add_data


@pytest.fixture
def get_document(db):
    def get(id):
        doc_ref = db.collection('test').document(id)
        doc = doc_ref.get().to_dict()
        return doc
    return get


@pytest.fixture
def all_doc_ids(db):
    ids = []

    count = 0
    count_list = -1
    while True:
        docs = db.collection('test').offset(count).limit(4).get()
        for doc in docs:
            ids.append(int(doc.id))
            count += 1

        if len(ids) == count_list:
            break
        count_list = len(ids)
    return ids
