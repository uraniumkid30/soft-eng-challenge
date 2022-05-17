from django.db import models


class BaseModel(models.Model):
    update = models.DateTimeField(null=True, blank=True)
    created = models.DateField(auto_now_add=True, blank=True, null=True)

    class Meta:
        abstract = True
