from settings import *
from firebase_orm.models.fields import *
from firebase_orm.models.base import Model
from firebase_orm.models.manager import Manager

import firebase_admin
from firebase_admin import storage, firestore

firebase_admin.initialize_app(
    firebase_admin.credentials.Certificate(CERTIFICATE), {
        'storageBucket': BUCKET_NAME
    }
)

if not Manager.db:
    Manager.db = firebase_admin.firestore.client()
    Manager.bucket = firebase_admin.storage.bucket()
