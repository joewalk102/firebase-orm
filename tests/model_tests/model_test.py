def test_equal_obj(model):
    """содержимое экземпляров равно"""
    inst = model.objects.get(id=1)
    inst1 = model.objects.get(id=1)
    assert inst == inst1


def test_not_equal_obj(model):
    """содержимое экземпляров не равно"""
    inst = model.objects.get(id=1)
    inst1 = model()
    assert inst != inst1


def test_repr(model):
    inst = model.objects.get(id=1)
    repr_str = f'<{type(inst).__name__}: {inst.__str__()}>'
    assert inst.__repr__() == repr_str
