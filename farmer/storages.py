# storages.py (직접 생성)
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class LocalImageStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        kwargs['location'] = os.path.join(settings.BASE_DIR, 'static', 'images', 'farminfo')
        kwargs['base_url'] = '/static/images/farminfo/'
        super().__init__(*args, **kwargs)
