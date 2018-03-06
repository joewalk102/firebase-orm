class TestTextStringType:
    def test_save_null_empty_str(self, model):
        """при сохранение пустой строки в поле, в базе появляется значение null"""
        model_null = model.objects.get(id=1)
        model_null.name = ''
        model_null.save()
        model_null = model.objects.get(id=1)
        assert model_null.name is None

    def test_save_null_str_of_spaces(self, model):
        """при сохранение строки с пробелами в поле, в базе появляется значение null"""
        model_null = model.objects.get(id=1)
        model_null.name = '  '
        model_null.save()
        model_null = model.objects.get(id=1)
        assert model_null.name is None


def test_create_inst(model):
    """Создание нового объекта модели"""
    inst = model()
    inst.save()
    pk = inst.id
    inst1 = model.objects.get(id=pk)
    assert inst == inst1
