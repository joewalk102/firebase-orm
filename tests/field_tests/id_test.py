import pytest

from firebase_orm.exceptions import CanNotBeChanged


class TestAutoFieldType:
    def test_id_type_int(self, model):
        """ID должен возвращаться типа int"""
        inst = model.objects.get(id=0)
        pk = inst.id
        assert type(pk) is int

    def test_id_type_not_int(self, model):
        with pytest.raises(TypeError):
            model.objects.get(id='0')


def test_present_in_the_database_document(get_document):
    pk = '0'
    doc = get_document(id=pk)
    assert doc.get('id') == int(pk)


def test_not_change_id(model):
    """id не изменяемый"""
    with pytest.raises(CanNotBeChanged):
        inst = model.objects.get(id=0)
        inst.id = 2


def test_id_unique(model, all_doc_ids):
    inst = model()
    inst.save()
    assert inst.id not in all_doc_ids


def test_id_autoincrement(model, all_doc_ids):
    pk = max(all_doc_ids)+1
    inst = model()
    inst.save()
    assert inst.id == pk


def test_pk0_if_non_existent_collection(new_collection):
    model = new_collection()
    inst = model()
    pk = inst.id
    assert pk == 0
