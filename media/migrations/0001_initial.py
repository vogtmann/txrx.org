# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-04-19 12:23
from __future__ import unicode_literals

import crop_override.field
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import lablackey.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MiscFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(editable=False, max_length=200)),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('upload_dt', models.DateTimeField(auto_now_add=True)),
                ('file', models.FileField(upload_to=b'uploads/file/%Y-%m')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(editable=False, max_length=200)),
                ('name', models.CharField(blank=True, max_length=500, null=True)),
                ('upload_dt', models.DateTimeField(auto_now_add=True)),
                ('file', crop_override.field.OriginalImage(max_length=200, null=True, upload_to=b'uploads/photos/%Y-%m', verbose_name=b'Photo')),
                ('caption', models.TextField(blank=True, null=True)),
                ('approved', models.BooleanField(default=False)),
                ('source', models.CharField(choices=[(b'web', b'Web'), (b'twittpic', b'TwittPic'), (b'email', b'Email'), (b'misc', b'Miscelaneous')], default=b'web', max_length=16)),
                ('square_crop', crop_override.field.CropOverride(blank=True, help_text=b'Usages: Blog Photo, Tool Photo', max_length=200, null=True, upload_to=b'uploads/photos/%Y-%m', verbose_name=b'Square Crop (1:1)')),
                ('landscape_crop', crop_override.field.CropOverride(blank=True, help_text=b'Usages: Featured Blog Photo, Lab Photo', max_length=200, null=True, upload_to=b'uploads/photos/%Y-%m', verbose_name=b'Landscape Crop (3:2)')),
                ('portrait_crop', crop_override.field.CropOverride(blank=True, help_text=b'Usages: None', max_length=200, null=True, upload_to=b'uploads/photos/%Y-%m', verbose_name=b'Portrait Crop (2:3)')),
                ('external_url', models.URLField(blank=True, null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='PhotoTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='TaggedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField()),
                ('order', models.IntegerField(default=9999)),
                ('private', models.BooleanField(default=False, help_text=b'Files will not appear until after the user has completed a class.')),
            ],
        ),
        migrations.CreateModel(
            name='TaggedPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.IntegerField()),
                ('order', models.IntegerField(default=9999)),
            ],
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('session_key', models.CharField(blank=True, max_length=40, null=True)),
                ('src', models.FileField(blank=True, max_length=200, null=True, storage=django.core.files.storage.FileSystemStorage(base_url=b'/media_files/private/', location=b'/home/chriscauley/txrx.org/.private'), upload_to=b'%Y%m')),
                ('name', models.CharField(max_length=256)),
                ('content_type', models.CharField(max_length=256)),
                ('session', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_mediauploadedfiles', to='sessions.Session')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, lablackey.db.models.JsonMixin),
        ),
    ]
