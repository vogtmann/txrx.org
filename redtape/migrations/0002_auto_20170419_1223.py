# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-04-19 12:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('redtape', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='signature',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='documentfield',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='redtape.Document'),
        ),
    ]
