# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-01-12 13:51
from __future__ import unicode_literals

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0022_auto_20170108_1113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signature',
            name='data',
            field=jsonfield.fields.JSONField(default=dict),
        ),
    ]
