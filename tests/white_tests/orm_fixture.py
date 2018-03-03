import pytest

from firebase_orm import models


class TModel(models.Model):
    name = models.CharField()
    type_test = models.CharField(db_column='type')
    author = models.CharField()
    brief = models.CharField()

    class Meta:
        db_table = 'test'

    def __str__(self):
        return self.name


@pytest.fixture
def model():
    return TModel
