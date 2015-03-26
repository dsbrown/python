# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_selection', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='foobar',
        ),
        migrations.AlterField(
            model_name='project',
            name='aws_type',
            field=models.ForeignKey(verbose_name=b'AWS type (AZ,Edge)', to='site_selection.AWS_Type'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='engr_id',
            field=models.ForeignKey(verbose_name=b'engineer login id', to='site_selection.Engineers'),
            preserve_default=True,
        ),
    ]
