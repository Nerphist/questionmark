from django.db import models


# Create your models here.
class AbstractCreateUpdateModel(models.Model):
    class Meta:
        abstract = True
        ordering = ['pk']

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
