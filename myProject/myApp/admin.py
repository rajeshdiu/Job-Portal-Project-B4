from django.contrib import admin

from myApp.models import *


class Custom_User_Display(admin.ModelAdmin):

    list_display=['username','email','user_type']


admin.site.register(Custom_User,Custom_User_Display)


class Job_Model_Display(admin.ModelAdmin):
    
    list_display=['job_title','salary','employment_type','company_name']
    
admin.site.register(JobModel,Job_Model_Display)


class jobApplyModel_Display(admin.ModelAdmin):
    
    list_display=['job','user','Full_Name','Work_Experience','Skills','Expected_Salary']
    
admin.site.register(jobApplyModel,jobApplyModel_Display)




