# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 23:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shortLinks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='links',
            old_name='link_short_id',
            new_name='links_short_id',
        ),
    ]
