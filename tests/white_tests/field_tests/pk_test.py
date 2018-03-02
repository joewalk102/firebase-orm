import pytest

from firebase_orm.exeptions import CanNotBeChanged


def test_id_type_int(model):
    """ID должен возвращаться типа int"""
    inst = model.objects.get(id=1)
    pk = inst.id
    assert type(pk) is int


def test_id_type_not_int(model):
    with pytest.raises(TypeError):
        model.objects.get(id='1')


def test_id_unique(model, all_doc_ids):
    """ID при создании объекта должен быть уникальным"""
    inst = model()
    inst.save()
    assert inst.id not in all_doc_ids


def test_append_id_to_id_docs(model, all_doc_ids):
    """id присваивается автоматически больше на еденицу id документов в базе"""
    pk = max(all_doc_ids)+1
    inst = model()
    inst.save()
    assert inst.id == pk


def test_fields_id_presents_in_doc(get_document):
    """id должен быть тип int и присутствовать в поле документа"""
    pk = '1'
    doc = get_document(id=pk)
    assert doc.get('id') == int(pk)


def test_not_change_id(model):
    with pytest.raises(CanNotBeChanged):
        inst = model.objects.get(id=1)
        inst.id = 2
