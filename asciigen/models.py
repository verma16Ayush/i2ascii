from django.db import models
from .settings import MEDIA_ROOT
import os

class Query(models.Model):
    name:models.CharField = models.CharField(max_length=200, null=False)
    email:models.EmailField = models.EmailField(null=False)
    img:models.ImageField = models.ImageField(default=os.path.join(MEDIA_ROOT, 'octocat.png'))

    def __str__(self):
        return self.email