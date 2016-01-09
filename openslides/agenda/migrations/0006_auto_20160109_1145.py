# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-09 11:45
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0005_auto_20151210_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='item',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='agenda.Item'),
        ),
    ]
