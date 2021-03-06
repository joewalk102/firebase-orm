import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

pytest_plugins = [
    "orm_fixture",
    "firebase_fixture",
    "model_tests.fixture"
]
