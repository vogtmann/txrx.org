# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-04-19 12:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import media.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tool', '__first__'),
        ('drop', '0006_auto_20170211_2031'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumable',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='drop.Product')),
                ('part_number', models.CharField(blank=True, max_length=32, null=True)),
                ('part_style', models.CharField(blank=True, max_length=32, null=True)),
                ('purchase_url', models.URLField(blank=True, max_length=1024, null=True)),
                ('purchase_url2', models.URLField(blank=True, max_length=1024, null=True)),
                ('in_stock', models.IntegerField(blank=True, help_text=b'Leave blank and this fill always show as in stock.', null=True)),
                ('purchase_quantity', models.IntegerField(default=1, help_text=b'Amount purchased (by us when restocking) at a time. Used to make the refill process quick.')),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(media.models.PhotosMixin, 'drop.product'),
        ),
        migrations.CreateModel(
            name='CourseCheckout',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='drop.Product')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course')),
            ],
            options={
                'abstract': False,
            },
            bases=(media.models.PhotosMixin, 'drop.product'),
        ),
        migrations.CreateModel(
            name='ToolConsumableGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('consumables', models.ManyToManyField(to='store.Consumable')),
                ('tools', models.ManyToManyField(to='tool.Tool')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
