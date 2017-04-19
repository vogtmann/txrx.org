# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-04-19 13:52
from __future__ import unicode_literals

import annoying.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import lablackey.db.models
import membership.models
import wmd.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ipn', '0007_auto_20160219_1135'),
        ('drop', '0006_auto_20170211_2031'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('media', '0002_auto_20170419_1223'),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
                ('status', models.CharField(choices=[(b'used', b'Used'), (b'staff', b'Staff'), (b'canceled', b'Needs Email'), (b'emailed', b'Emailed'), (b'maintenance', b'Maintenance'), (b'open', b'Open')], default=b'used', help_text=b'Automatically set when changes are made to subscription or container via admin.', max_length=16)),
                ('kind', models.CharField(choices=[(b'drawer', b'Drawer'), (b'table', b'Table'), (b'bay', b'Bay'), (b'studio', b'Studio')], default=b'bay', max_length=64)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ('room', 'number'),
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=128)),
            ],
            options={
                'ordering': ('text',),
            },
        ),
        migrations.CreateModel(
            name='Flag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[(b'recurring_payment_skipped', b'PayPal Skipped'), (b'recurring_payment_failed', b'PayPal Failed Recurring'), (b'recurring_payment_suspended', b'PayPal Suspended'), (b'recurring_payment_suspended_due_to_max_failed_payment', b'PayPal Max Failed Payment'), (b'subscr_failed', b'PayPal Failed Subscription'), (b'subscr_eot', b'PayPal End of Term'), (b'manually_flagged', b'Manually Flagged'), (b'safety', b'Expiring Safety Criterion'), (b'subscr_cancel', b'Paypal Canceled')], max_length=64)),
                ('status', models.CharField(choices=[(b'new', b'New'), (b'first_warning', b'Warned Once'), (b'second_warning', b'Warned Twice'), (b'final_warning', b'Canceled (Automatically)'), (b'canceled', b'Canceled (Manually)'), (b'resolved', b'Resolved'), (b'paid', b'Paid'), (b'safety_new', b'New'), (b'safety_emailed', b'Emailed'), (b'safety_expired', b'Expired (criterion revoked)'), (b'safety_completed', b'Completed (course taken)')], default=b'new', max_length=32)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('emailed', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('order', models.IntegerField(verbose_name=b'Level')),
                ('discount_percentage', models.IntegerField(default=0)),
                ('permission_description', models.TextField(blank=True, default=b'')),
                ('machine_credits', models.IntegerField(default=0)),
                ('simultaneous_users', models.IntegerField(default=0)),
                ('cost_per_credit', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('custom_training_cost', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('custom_training_max', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('holiday_access', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Membership Level',
            },
        ),
        migrations.CreateModel(
            name='LevelDoorGroupSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'ordering': ('level',),
            },
        ),
        migrations.CreateModel(
            name='LimitedAccessKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(max_length=32, unique=True)),
                ('expires', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, lablackey.db.models.JsonMixin),
        ),
        migrations.CreateModel(
            name='MeetingMinutes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, unique=True)),
                ('content', wmd.models.MarkDownField()),
                ('member_count', models.IntegerField(default=0, help_text=b'Used only when an exact list of members is unavailable (eg legacy minutes)')),
                ('inactive_present', models.ManyToManyField(blank=True, related_name='meetings_inactive', to=settings.AUTH_USER_MODEL)),
                ('nonvoters_present', models.ManyToManyField(blank=True, related_name='_meetingminutes_nonvoters_present_+', to=settings.AUTH_USER_MODEL)),
                ('voters_present', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-date',),
            },
        ),
        migrations.CreateModel(
            name='MembershipFeature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=0)),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.Feature')),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.Level')),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='Officer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('position', models.CharField(max_length=50)),
                ('start', models.DateField(default=datetime.date.today)),
                ('end', models.DateField(blank=True, null=True)),
                ('order', models.IntegerField(default=999)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('order', 'end'),
            },
            bases=(models.Model, lablackey.db.models.JsonMixin),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='drop.Product')),
                ('months', models.IntegerField(choices=[(1, b'Monthly'), (3, b'Quarterly'), (6, b'Biannually'), (12, b'Yearly')], default=1)),
                ('order', models.IntegerField(default=0)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.Level')),
            ],
            options={
                'ordering': ('order',),
            },
            bases=('drop.product',),
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(default=0)),
                ('title', models.CharField(blank=True, max_length=256, null=True)),
                ('original', wmd.models.MarkDownField()),
                ('ammended', wmd.models.MarkDownField(blank=True, null=True)),
                ('meeting_minutes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.MeetingMinutes')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('order',),
            },
            bases=(models.Model, lablackey.db.models.JsonMixin),
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('payment_method', models.CharField(choices=[(b'paypal', b'PayPalIPN'), (b'cash', b'Cash/Check'), (b'adjustment', b'Adjustment (gift from lab)'), (b'refund', b'Refund'), (b'legacy', b'Legacy (PayPal)')], default=b'cash', max_length=16)),
                ('notes', models.CharField(blank=True, max_length=128, null=True)),
                ('datetime', models.DateTimeField(default=datetime.datetime.now)),
                ('transaction_id', models.CharField(blank=True, max_length=32, null=True)),
                ('paypalipn', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ipn.PayPalIPN')),
            ],
            options={
                'ordering': ('datetime',),
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscr_id', models.CharField(blank=True, help_text=b'Only used with PayPal subscriptions. Do not touch.', max_length=20, null=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('canceled', models.DateTimeField(blank=True, null=True)),
                ('paid_until', models.DateTimeField(blank=True, null=True)),
                ('months', models.IntegerField(choices=[(1, b'Monthly'), (3, b'Quarterly'), (6, b'Biannually'), (12, b'Yearly')], default=1)),
                ('amount', models.DecimalField(decimal_places=2, default=0, help_text=b'If zero, this membership will always be active until deleted.', max_digits=30)),
                ('owed', models.DecimalField(decimal_places=2, default=0, max_digits=30)),
                ('level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='membership.Level')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='SubscriptionBuddy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid_until', models.DateTimeField(blank=True, null=True)),
                ('level_override', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='membership.Level')),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.Subscription')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voting_rights', models.BooleanField(default=False)),
                ('suspended', models.BooleanField(default=False)),
                ('bio', wmd.models.MarkDownField(blank=True, null=True)),
                ('api_key', models.CharField(default=membership.models.rand32, max_length=32)),
                ('by_line', models.CharField(blank=True, help_text=b'A short description of what you do for the lab.', max_length=50, null=True)),
                ('notify_global', models.BooleanField(default=True, help_text=b'Uncheck this to stop all correspondance from this website (same as setting all of the following to "Do not notify me about this")', verbose_name=b'Global Email Preference')),
                ('notify_comments', models.BooleanField(default=True, help_text=b'If checked, you will be emailed whenever someone replies to a comment you make on this site.', verbose_name=b'Comment Response Email')),
                ('notify_classes', models.BooleanField(default=True, help_text=b"If checked, you will be emailed a reminder 24 hours before a class (that you've signed up for).", verbose_name=b'Class Reminder Email')),
                ('notify_sessions', models.BooleanField(default=True, help_text=b'If checked, you will be emailed new class offerings (twice a month).', verbose_name=b'New Course Email')),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='media.Photo')),
                ('user', annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='status',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='membership.Subscription'),
        ),
    ]
