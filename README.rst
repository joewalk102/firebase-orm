FirebaseORM Python
=======================================
Django like models for NoSQL database Firestore.

________

Installation
============

.. code-block:: shell

    $ pip install firebase_orm

Initialize
==========

Create settings.py in the root directory of the project:

    settings.py

    .. code-block:: python

        CERTIFICATE = 'path/to/serviceAccountKey.json'
        BUCKET_NAME = '<BUCKET_NAME>.appspot.com'

CERTIFICATE
    Once you have created a `Firebase console <https://console.firebase.google.com/?authuser=0>`_ project and downloaded a JSON file with your service account credentials.

BUCKET_NAME
    The bucket name must not contain gs:// or any other protocol prefixes. For example, if the bucket URL displayed in the `Firebase console <https://console.firebase.google.com/?authuser=0>`_ is gs://bucket-name.appspot.com, pass the string bucket-name.appspot.com

Usage
======

Create model:
"""""""""""""

.. code-block:: python

    from firebase_orm import models


    class Article(models.Model):
        headline = models.TextString()
        type_article = models.TextString(db_column='type')

        class Meta:
            db_table = 'medications'

        def __str__(self):
            return self.headline

Use API:
""""""""
**Creating objects**

To represent cloud firestore data in Python objects, FirebaseORM uses an intuitive system:
A model class represents a collection,
and an instance of that class represents a document in collection.

To create an object, instantiate it using keyword arguments to the model class,
then call save() to save it to the database.

.. code-block:: pycon

    # Import the models we created
    >>> from models import Article
    # Create a new Article.
    >>> a = Article(headline='Django is cool')
    # Save the object into the database. You have to call save() explicitly.
    >>> a.save()


.. code-block:: pycon

    # Now it has an ID.
    >>> a.id
    1

    # Fields are represented as attributes on the Python object.
    >>> a.headline
    'Django is cool'

    # Firebase ORM provides a rich database lookup API.
    >>> Article.objects.get(id=1)
    <Article: Django is cool>
    >>> Article.objects.get(id=2)
    Traceback (most recent call last):
        ...
    DoesNotExist: Article matching query does not exist.



Field options:
==============

The following arguments are available to all field types. All are optional.

**Field.db_column**

    If contains characters that aren’t allowed in Python variable names – use db_column.
    The name of the firestore key in document to use for this field.
    If this isn’t given, FirebaseORM will use the field’s name.


Field types:
============

AutoField
"""""""""
**class AutoField()**

    By default, FirebaseORM gives each model the following field:

    .. code-block:: python

        id = models.AutoField(primary_key=True)

TextString
""""""""""
**class TextString(**options)**

    Text string Up to 1,048,487 bytes (1 MiB - 89 bytes).
    Only the first 1,500 bytes of the UTF-8 representation are considered by queries.

    TextString has not extra required argument.
