from firebase_orm.models import Manager


def monkey_data(self, id):
    return {'name': 'monkey'}


def test_id_if_objects_get(model, monkeypatch):
    monkeypatch.setattr(Manager, '_get_data', monkey_data)
    inst = model.objects.get(id=1)
    monkeypatch.undo()
    assert inst.name == 'monkey'


def test_id_if_create_instance(model, monkeypatch):
    pk = 4

    def monkey_id(self):
        return pk
    monkeypatch.setattr(Manager, '_id_autoincrement', monkey_id)

    inst = model()

    monkeypatch.undo()
    assert inst.id == pk


def test_repr(model, monkeypatch):
    monkeypatch.setattr(Manager, '_get_data', monkey_data)
    inst = model.objects.get(id=1)
    repr_str = f'<{type(inst).__name__}: {inst.__str__()}>'
    monkeypatch.undo()
    assert inst.__repr__() == repr_str
