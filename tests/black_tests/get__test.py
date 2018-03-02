import pytest


def test_kwarg_error(model):
    with pytest.raises(TypeError):
        model.objects.get(100)
