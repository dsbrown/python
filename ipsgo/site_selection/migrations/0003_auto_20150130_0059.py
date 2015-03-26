# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_selection', '0002_auto_20150130_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='assessment_date',
            field=models.DateField(null=True, verbose_name=b'date of assessment', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='fnl_rpt_date',
            field=models.DateField(null=True, verbose_name=b'date of final report delivery', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='phase1_score',
            field=models.DecimalField(null=True, verbose_name=b'composite phase 1 site score', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='phase2_score',
            field=models.DecimalField(null=True, verbose_name=b'composite phase 2 site score', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='pre_rpt_date',
            field=models.DateField(null=True, verbose_name=b'date of preliminary report delivery', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='site_delivery_cost',
            field=models.DecimalField(null=True, verbose_name=b'region/site delivery estimated effort (cost)', max_digits=10, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='site_delivery_date',
            field=models.DateField(null=True, verbose_name=b'site infrastructure delivery accepted date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='site_delivery_hours',
            field=models.DecimalField(null=True, verbose_name=b'region/site delivery estimated effort (hours)', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='trip_cost',
            field=models.DecimalField(null=True, verbose_name=b'regional/site assessment trip cost', max_digits=10, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='trip_hours',
            field=models.DecimalField(null=True, verbose_name=b'regional site assessment estimated effort (hours)', max_digits=10, decimal_places=1, blank=True),
            preserve_default=True,
        ),
    ]
