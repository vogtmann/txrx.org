# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2017-02-21 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notify', '0004_auto_20170221_1329'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='notifycourse',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='notifycourse',
            name='course',
        ),
        migrations.RemoveField(
            model_name='notifycourse',
            name='user',
        ),
        migrations.AddField(
            model_name='notification',
            name='target_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='target_type',
            field=models.CharField(blank=True, max_length=201, null=True),
        ),
        migrations.DeleteModel(
            name='NotifyCourse',
        ),
    ]
