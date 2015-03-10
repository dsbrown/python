# Create your models here.
import datetime

from django.db import models
from django.utils import timezone

class AWS_Type(models.Model):
    aws_type = models.CharField('AWS type (az,edge)',max_length=32, unique=True)


class Engineers(models.Model):
    engr_id = models.CharField('engineer login id',max_length=64, unique=True)

class Project(models.Model):
    creation_date = models.DateTimeField('record creation time',auto_now_add=True)
    #creation_date.editable = True
    modify_date = models.DateTimeField('record modification time',default=timezone.now)
    modify_date.editable = True
    cluster_name = models.CharField('cluster name',max_length=3)
    site_number = models.IntegerField('site number',default=0)
    project_id = models.AutoField('project id',unique=True)
    engr_id = models.ForeignKey(Engineers, verbose_name='AWS type (AZ,Edge)')
    aws_type = models.ForeignKey(AWS_Type, verbose_name='engineer login id')
    vendor_name	= models.CharField('vendor name',max_length=80)
    site_address = models.CharField('site address',max_length=200)
    biz_dev_rep_id = models.CharField('business development rep login id',max_length=64)
    assessment_date	= models.DateField('date of assessment',blank=true)
    pre_rpt_date = models.DateField('date of preliminary report delivery',blank=true)
    fnl_rpt_date =  models.DateField('date of final report delivery',blank=true)
    trip_cost = models.DecimalField('regional/site assessment trip cost',blank=true)
    trip_hours = models.DecimalField('regional site assessment estimated effort (hours)',blank=true)
    phase1_score = models.DecimalField('composite phase 1 site score',blank=true)
    phase2_score = models.DecimalField('composite phase 2 site score',blank=true),
    site_recommended = models.NullBooleanField('site recommended by you?',blank=true)
    site_selected_biz = models.NullBooleanField('selected site by biz?',blank=true)
    site_delivery_cost = models.DecimalField('region/site delivery estimated effort (cost)',blank=true)
    site_delivery_hours = models.DecimalField('region/site delivery estimated effort (hours)',blank=true)
    site_delivery_date = models.DateField('site infrastructure delivery accepted date',blank=true)
    
     def __unicode__(self):
        return self.cluster_name + "-" + self.site_number
    