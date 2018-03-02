from firebase_orm.models.fields import *
from firebase_orm.models.base import Model
import firebase_admin
from firebase_admin import credentials, firestore, storage
from settings import *

from firebase_orm.models.manager import Manager


cred = credentials.Certificate(CERTIFICATE)
firebase_admin.initialize_app(cred, {
    'storageBucket': BUCKET_NAME
})
if not Manager.db:
    Manager.db = firestore.client()
    Manager.bucket = storage.bucket()

