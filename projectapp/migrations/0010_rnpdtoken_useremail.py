# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-09-14 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectapp', '0009_remove_rnpdtoken_useremail'),
    ]

    operations = [
        migrations.AddField(
            model_name='rnpdtoken',
            name='useremail',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]