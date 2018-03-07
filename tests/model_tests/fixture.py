import pytest
import random
import string
from firebase_orm import models

VOWELS = "aeiou"
CONSONANTS = "".join(set(string.ascii_lowercase) - set(VOWELS))


@pytest.fixture
def random_name():
    def generate_word():
        word = ""
        for i in range(8):
            if i % 2 == 0:
                word += random.choice(CONSONANTS)
            else:
                word += random.choice(VOWELS)
        return word

    return generate_word


names = []


@pytest.fixture
def new_collection(random_name, del_all):
    def return_model():
        global names
        name = random_name()
        names.append(name)

        class Model(models.Model):
            type_test = models.TextString(db_column='type')

            class Meta:
                db_table = name

        return Model
    try:
        yield return_model
    finally:
        for i in names:
            del_all(i)
