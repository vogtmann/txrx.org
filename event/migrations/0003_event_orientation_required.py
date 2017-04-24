# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-04-24 13:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0002_auto_20170419_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='orientation_required',
            field=models.BooleanField(default=False, help_text=b'If true, members cannot RSVP unless they have been through the orientation.'),
        ),
    ]
