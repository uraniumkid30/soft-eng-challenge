from django.db import models


class BaseModel(models.Model):
    update = models.DateTimeField(auto_now=True, null=True, blank=True)
    created = models.DateField(auto_now_add=True, blank=True, null=True)

    class Meta:
        abstract = True
