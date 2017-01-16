# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-24 22:45
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models
import lablackey.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('redtape', '0017_auto_20160826_1633'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.FileField(blank=True, max_length=200, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'', location=b'/home/chriscauley/txrx.org/main/../.private'), upload_to=b'%Y%m')),
                ('name', models.CharField(max_length=256)),
                ('content_type', models.CharField(max_length=256)),
            ],
            bases=(models.Model, lablackey.db.models.UserOrSessionMixin),
        ),
        migrations.AlterField(
            model_name='documentfield',
            name='input_type',
            field=models.CharField(choices=[(b'text', b'Text'), (b'number', b'Number'), (b'phone', b'Phone'), (b'email', b'Email'), (b'header', b'Design Element (non-input)'), (b'select', b'Select'), (b'checkbox-input', b'Select Multiple'), (b'signature', b'Sign Your Name'), (b'checkbox', b'Checkbox'), (b'textarea', b'Textarea (multi-line)'), (b'multi-file', b'Multiple File')], max_length=64),
        ),
    ]