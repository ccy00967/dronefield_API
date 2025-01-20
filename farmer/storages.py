# storages.py (직접 생성)
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class LocalImageStorage(FileSystemStorage):
    def __init__(self, *args, **kwargs):
        # 기본적으로 MEDIA_ROOT를 기준으로 파일을 저장
        kwargs['location'] = kwargs.get('location', settings.MEDIA_ROOT)
        kwargs['base_url'] = kwargs.get('base_url', settings.MEDIA_URL)
        super().__init__(*args, **kwargs)