# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('common', '0002_auto_20150430_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='confirmation',
            name='author',
        ),
    ]