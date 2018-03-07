import pytest

from firebase_orm.exeptions import DoesNotExist


def test_error_kwarg(model):
    with pytest.raises(TypeError):
        model.objects.get(100)


@pytest.mark.run(order=2)
def test_get(add_document, model):
    pk = "0"
    add_document(pk)
    test_model = model.objects.get(id=int(pk))
    assert test_model.id == int(pk)


@pytest.mark.run(order=1)
def test_object_does_not_exist(model):
    with pytest.raises(DoesNotExist):
        model.objects.get(id=100)
