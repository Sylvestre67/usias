# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-11 03:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_proposal_uuidmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposal',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]