# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-09-13 15:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_event_orientation_required'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('name',)},
        ),
    ]
