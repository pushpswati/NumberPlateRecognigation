# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-08-28 11:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0004_auto_20180824_0838'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rnpdtoken',
            old_name='token_key',
            new_name='token_key1',
        ),
    ]
