from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class Notice(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, blank=True, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Notice")

    def __str__(self):
        return self.title

class Alarm(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, blank=True, null=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Alarm")

    def __str__(self):
        return self.title

class TestDocument(models.Model):
    file = models.FileField(upload_to='test_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
