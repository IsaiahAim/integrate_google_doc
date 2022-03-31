from django.db import models
import uuid

from core import settings

PROVIDER_TYPE = (
    ('GOOGLE', 'GOOGLE'),
    ('MICROSOFT', 'MICROSOFT')
)


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Memo(Base):
    title = models.CharField(max_length=200, unique=True)
    url = models.URLField()
    provider = models.CharField(max_length=100, choices=PROVIDER_TYPE)
    document_id = models.CharField(max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name="memo_creator")

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.title}'


class Template(Base):
    name = models.CharField(max_length=200, unique=True)
    url = models.URLField()
    document_id = models.CharField(max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                   null=True, related_name="template_creator")
    provider = models.CharField(max_length=100, choices=PROVIDER_TYPE)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.name}'
