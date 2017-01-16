# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-28 17:19
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0018_auto_20161224_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentfield',
            name='input_type',
            field=models.CharField(choices=[(b'text', b'Text'), (b'textarea', b'Textarea (multi-line)'), (b'number', b'Number'), (b'phone', b'Phone'), (b'email', b'Email'), (b'header', b'Design Element (non-input)'), (b'checkbox', b'Checkbox'), (b'select', b'Select'), (b'checkbox-input', b'Select Multiple'), (b'signature', b'Sign Your Name'), (b'multi-file', b'Multiple File')], max_length=64),
        ),
        migrations.AlterField(
            model_name='uploadedfile',
            name='src',
            field=models.FileField(blank=True, max_length=200, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/redtape/file/', location=b'/home/chriscauley/txrx.org/.private'), upload_to=b'%Y%m'),
        ),
    ]