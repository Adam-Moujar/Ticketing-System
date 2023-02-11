from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify


class Department(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    slug = models.SlugField(max_length=100)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
