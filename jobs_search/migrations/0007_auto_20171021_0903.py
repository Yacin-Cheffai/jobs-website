# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-21 08:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs_search', '0006_auto_20171020_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annonce',
            name='description',
            field=models.TextField(max_length=1500),
        ),
        migrations.AlterField(
            model_name='annonce',
            name='domaine',
            field=models.CharField(choices=[('technology', 'technology'), ('mechanics', 'mechanics'), ('commerce', 'commerce'), ('training and education', 'training and education'), ('services', 'services'), ('tourism', 'tourism')], default=1, max_length=100),
        ),
    ]
