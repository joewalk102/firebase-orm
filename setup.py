from setuptools import setup, find_packages

import firebase_orm

setup(
    name='firebase_orm',
    version=firebase_orm.__version__,
    description='NoSQL object model database',
    author='Vladimir Filipenko',
    author_email='zavx0z@ya.ru',
    url='https://github.com/zavx0z/firebase_orm',
    packages=find_packages(),
    long_description=open('README.rst').read(),
    install_requires=[
        'firebase-admin>=2.9.0',
        'grpcio>=1.9.1'
    ],
    test_suite='tests',
    license='MIT',
)
