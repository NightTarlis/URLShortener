# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-01 21:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortLinks', '0009_auto_20160901_2031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='links',
            name='id',
        ),
        migrations.AlterField(
            model_name='links',
            name='links_short',
            field=models.SlugField(primary_key=True, serialize=False),
        ),
    ]
