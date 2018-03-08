import pytest

from firebase_orm import models


class TModel(models.Model):
    name = models.TextField()
    type_test = models.TextField(db_column='type')

    class Meta:
        db_table = 'test'

    def __str__(self):
        return str(self.name)


@pytest.fixture
def model():
    return TModel
