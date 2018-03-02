import os
import sys

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

pytest_plugins = [
    "white_tests.orm_fixture",
    "white_tests.firebase_fixture",

    "black_tests.fixture"
]
