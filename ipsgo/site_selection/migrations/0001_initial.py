# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AWS_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('aws_type', models.CharField(unique=True, max_length=32, verbose_name=b'AWS type (az,edge)')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Engineers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('engr_id', models.CharField(unique=True, max_length=64, verbose_name=b'engineer login id')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name=b'record creation time')),
                ('modify_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'record modification time')),
                ('cluster_name', models.CharField(max_length=3, verbose_name=b'cluster name')),
                ('site_number', models.IntegerField(default=0, verbose_name=b'site number')),
                ('vendor_name', models.CharField(max_length=80, verbose_name=b'vendor name')),
                ('site_address', models.CharField(max_length=200, verbose_name=b'site address')),
                ('biz_dev_rep_id', models.CharField(max_length=64, verbose_name=b'business development rep login id')),
                ('assessment_date', models.DateField(verbose_name=b'date of assessment', blank=True)),
                ('pre_rpt_date', models.DateField(verbose_name=b'date of preliminary report delivery', blank=True)),
                ('fnl_rpt_date', models.DateField(verbose_name=b'date of final report delivery', blank=True)),
                ('trip_cost', models.DecimalField(verbose_name=b'regional/site assessment trip cost', max_digits=10, decimal_places=2, blank=True)),
                ('trip_hours', models.DecimalField(verbose_name=b'regional site assessment estimated effort (hours)', max_digits=10, decimal_places=1, blank=True)),
                ('phase1_score', models.DecimalField(verbose_name=b'composite phase 1 site score', max_digits=10, decimal_places=1, blank=True)),
                ('phase2_score', models.DecimalField(verbose_name=b'composite phase 2 site score', max_digits=10, decimal_places=1, blank=True)),
                ('site_recommended', models.NullBooleanField(verbose_name=b'site recommended by you?')),
                ('site_selected_biz', models.NullBooleanField(verbose_name=b'selected site by biz?')),
                ('site_delivery_cost', models.DecimalField(verbose_name=b'region/site delivery estimated effort (cost)', max_digits=10, decimal_places=2, blank=True)),
                ('site_delivery_hours', models.DecimalField(verbose_name=b'region/site delivery estimated effort (hours)', max_digits=10, decimal_places=1, blank=True)),
                ('site_delivery_date', models.DateField(verbose_name=b'site infrastructure delivery accepted date', blank=True)),
                ('foobar', models.DateField()),
                ('aws_type', models.ForeignKey(verbose_name=b'engineer login id', to='site_selection.AWS_Type')),
                ('engr_id', models.ForeignKey(verbose_name=b'AWS type (AZ,Edge)', to='site_selection.Engineers')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
