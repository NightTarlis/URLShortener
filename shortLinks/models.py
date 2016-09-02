from django.db import models
from django.contrib.auth.models import User



class Links(models.Model):
    class Meta:
        db_table = 'Links'
    links_short = models.SlugField(max_length=50, primary_key=True)
    links_http = models.URLField(max_length=255, default='')
    links_count = models.IntegerField(default=0)
    links_login = models.CharField(max_length=50, default='')

