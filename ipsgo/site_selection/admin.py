from django.contrib import admin

# Register your models here.
from site_selection.models import Project, Engineers, AWS_Type

    
class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Project Descripton', {'fields': [
        'cluster_name',
        'site_number',
        'engr_id',
        'aws_type',
        'vendor_name',
        'site_address',
        'biz_dev_rep_id',
        ]}),
        ('Assessment', {'fields': [
        'assessment_date',
        'pre_rpt_date',
        'fnl_rpt_date',
        'trip_cost',
        'trip_hours',
        'phase1_score',
        'phase2_score',
        'site_recommended',
        'site_selected_biz',
        ]}),
        ('Site Delivery', {'fields': [
        'site_delivery_cost',
        'site_delivery_hours',
        'site_delivery_date',
        ]}),
    ]    

admin.site.register(Project,ProjectAdmin)
admin.site.register(Engineers) 
admin.site.register(AWS_Type)

