import pytest

from firebase_orm import models as m


class TModel(m.Model):
    name = m.TextString()
    type_test = m.TextString(db_column='type')

    class Meta:
        db_table = 'test'

    def __str__(self):
        return self.name


@pytest.fixture
def model():
    return TModel


class TModel2(m.Model):
    name = m.TextString()
    type_test = m.TextString(db_column='type')

    class Meta:
        db_table = 'test2'

    def __str__(self):
        return self.name


@pytest.fixture
def model2():
    return TModel2


@pytest.fixture
def models():
    return m
