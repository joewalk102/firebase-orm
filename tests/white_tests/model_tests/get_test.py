import pytest

from firebase_orm.exeptions import DoesNotExist


@pytest.mark.run(order=2)
# @pytest.mark.cloud
def test_get(add_document, model):
    pk = "1"
    add_document(pk)
    test_model = model.objects.get(id=1)
    assert test_model.id == int(pk)


@pytest.mark.run(order=1)
# @pytest.mark.cloud
def test_object_does_not_exist(model):
    with pytest.raises(DoesNotExist):
        model.objects.get(id=100)
