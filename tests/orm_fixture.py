import pytest

from firebase_orm import models


class TModel(models.Model):
    name = models.TextString()
    type_test = models.TextString(db_column='type')

    class Meta:
        db_table = 'test'

    def __str__(self):
        return str(self.name)


@pytest.fixture
def model():
    return TModel
