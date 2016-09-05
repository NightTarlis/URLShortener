from django.db import models
from django.contrib.auth.models import User


class Link(models.Model):
    short = models.SlugField(max_length=50)
    full = models.URLField(max_length=4000)
    count = models.IntegerField(default=0)
    login = models.CharField(max_length=50)

