# Create your models here.
import datetime

from django.db import models
from django.utils import timezone

class AWS_Type(models.Model):
    aws_type = models.CharField('AWS type (az,edge)',max_length=32, unique=True)
    
    def __unicode__(self):
        return self.aws_type

class Engineers(models.Model):
    engr_id = models.CharField('engineer login id',max_length=64, unique=True)
    
    def __unicode__(self):
        return self.engr_id

class Project(models.Model):
    creation_date = models.DateTimeField('record creation time',auto_now_add=True)
    #creation_date.editable = True
    modify_date = models.DateTimeField('record modification time',default=timezone.now)
    modify_date.editable = True
    cluster_name = models.CharField('cluster name',max_length=3)
    site_number = models.IntegerField('site number',default=0)
    #project_id = models.AutoField('project id',unique=True)
    engr_id = models.ForeignKey(Engineers, verbose_name='engineer login id')
    aws_type = models.ForeignKey(AWS_Type, verbose_name='AWS type (AZ,Edge)')
    vendor_name	= models.CharField('vendor name',max_length=80)
    site_address = models.CharField('site address',max_length=200)
    biz_dev_rep_id = models.CharField('business development rep login id',max_length=64)
    assessment_date	= models.DateField('date of assessment',blank=True,null=True)
    pre_rpt_date = models.DateField('date of preliminary report delivery',blank=True,null=True)
    fnl_rpt_date =  models.DateField('date of final report delivery',blank=True,null=True)
    trip_cost = models.DecimalField('regional/site assessment trip cost',blank=True,null=True,max_digits=10, decimal_places=2)
    trip_hours = models.DecimalField('regional site assessment estimated effort (hours)',blank=True,null=True,max_digits=10, decimal_places=1)
    phase1_score = models.DecimalField('composite phase 1 site score',blank=True,null=True,max_digits=10, decimal_places=1)
    phase2_score = models.DecimalField('composite phase 2 site score',blank=True,null=True,max_digits=10, decimal_places=1)
    site_recommended = models.NullBooleanField('site recommended by you?',blank=True,null=True)
    site_selected_biz = models.NullBooleanField('selected site by biz?',blank=True,null=True)
    site_delivery_cost = models.DecimalField('region/site delivery estimated effort (cost)',blank=True,null=True,max_digits=10, decimal_places=2)
    site_delivery_hours = models.DecimalField('region/site delivery estimated effort (hours)',blank=True,null=True,max_digits=10, decimal_places=1)
    site_delivery_date = models.DateField('site infrastructure delivery accepted date',blank=True,null=True)

    
    def __unicode__(self):
        return '{0}-{1}'.format(self.cluster_name, self.site_number)
    