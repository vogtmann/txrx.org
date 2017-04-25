# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-04-19 13:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tool', '0001_initial'),
        ('membership', '0001_initial'),
        ('geo', '0002_auto_20170419_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='leveldoorgroupschedule',
            name='doorgroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tool.DoorGroup'),
        ),
        migrations.AddField(
            model_name='leveldoorgroupschedule',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.Level'),
        ),
        migrations.AddField(
            model_name='leveldoorgroupschedule',
            name='schedule',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tool.Schedule'),
        ),
        migrations.AddField(
            model_name='level',
            name='door_schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='tool.Schedule'),
        ),
        migrations.AddField(
            model_name='level',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='membership.Group'),
        ),
        migrations.AddField(
            model_name='level',
            name='tool_schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='tool.Schedule'),
        ),
        migrations.AddField(
            model_name='flag',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.Subscription'),
        ),
        migrations.AddField(
            model_name='container',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.Room'),
        ),
        migrations.AddField(
            model_name='container',
            name='subscription',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='membership.Subscription'),
        ),
        migrations.AlterUniqueTogether(
            name='leveldoorgroupschedule',
            unique_together=set([('level', 'doorgroup')]),
        ),
    ]