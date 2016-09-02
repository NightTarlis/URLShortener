# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 23:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_short_id', models.CharField(default=0, max_length=255)),
                ('links_http', models.URLField(default=0, max_length=255)),
                ('links_count', models.IntegerField(default=0)),
                ('links_login', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]