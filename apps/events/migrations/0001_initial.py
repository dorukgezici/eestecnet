# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

import common.util


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_auto_20150516_1851'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseEvent',
            fields=[
                ('applicable_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='common.Applicable')),
                ('deadline', models.DateTimeField(null=True, blank=True)),
                ('unofficial_fee', models.IntegerField(null=True, blank=True)),
                ('max_participants', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('common.applicable', common.util.Reversable),
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='events.BaseEvent')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('location', models.CharField(max_length=200)),
                ('participation_fee', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
            bases=('events.baseevent', models.Model),
        ),
        migrations.CreateModel(
            name='ParticipationConfirmation',
            fields=[
                ('confirmation_ptr', models.OneToOneField(parent_link=True, auto_created=True, to='common.Confirmation')),
                ('confirmable_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='common.Confirmable')),
            ],
            options={
                'abstract': False,
            },
            bases=('common.confirmable', 'common.confirmation', object),
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='events.BaseEvent')),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('events.baseevent', models.Model),
        ),
        migrations.CreateModel(
            name='Travel',
            fields=[
                ('notification_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='common.Notification')),
                ('arrival_datetime', models.DateTimeField()),
                ('arrival_mode', models.CharField(max_length=100, choices=[(b'bus', b'bus'), (b'plane', b'plane'), (b'ship', b'ship'), (b'car', b'car'), (b'parachute', b'parachute')])),
                ('departure_datetime', models.DateTimeField()),
                ('departure_mode', models.CharField(max_length=100, choices=[(b'bus', b'bus'), (b'plane', b'plane'), (b'ship', b'ship'), (b'car', b'car'), (b'parachute', b'parachute')])),
                ('comment', models.TextField(null=True, blank=True)),
                ('participation', models.OneToOneField(to='accounts.Participation')),
            ],
            options={
                'abstract': False,
            },
            bases=('common.notification', common.util.Reversable),
        ),
        migrations.CreateModel(
            name='Workshop',
            fields=[
                ('baseevent_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='events.BaseEvent')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('location', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
            bases=('events.baseevent', models.Model),
        ),
        migrations.AddField(
            model_name='baseevent',
            name='owner',
            field=models.ForeignKey(editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
