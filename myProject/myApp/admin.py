from django.contrib import admin
from myApp.models import *

@admin.register(Custom_User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'first_name', 'last_name')
    search_fields = ('username', 'email')
    list_filter = ('user_type',)

@admin.register(JobModel)
class JobModelAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company_name', 'location', 'employment_type', 'posted_date')
    search_fields = ('job_title', 'company_name', 'location')
    list_filter = ('employment_type', 'posted_date')

@admin.register(jobApplyModel)
class JobApplyModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'Expected_Salary')
    search_fields = ('user__username', 'job__job_title', 'status')
    list_filter = ('status',)

@admin.register(MessageModel)
class MessageModelAdmin(admin.ModelAdmin):
    list_display = ('application', 'sender', 'recipient', 'timestamp')
    search_fields = ('application__Full_Name', 'sender__username', 'recipient__username')
    list_filter = ('timestamp',)

@admin.register(BasicInfoModel)
class BasicInfoModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'contact_No', 'Designation', 'Carrer_Summary')
    search_fields = ('user__username', 'Designation')
    
@admin.register(ExperienceModel)
class ExperienceModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'company_name', 'start_date', 'end_date')
    search_fields = ('user__username', 'job_title', 'company_name')
    list_filter = ('start_date', 'end_date')

@admin.register(InterestModel)
class InterestModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'name')
    search_fields = ('user__username', 'name')

@admin.register(FieldOfStudyModel)
class FieldOfStudyModelAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(DegreeModel)
class DegreeModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'level')
    search_fields = ('name',)

@admin.register(InstituteNameModel)
class InstituteNameModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state')
    search_fields = ('name', 'city')

@admin.register(EducationModel)
class EducationModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'institution_name', 'degree', 'start_date', 'end_date')
    search_fields = ('user__username', 'institution_name', 'degree')

@admin.register(IntermediateLanguageModel)
class IntermediateLanguageModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'Language_Name')
    search_fields = ('user__username', 'Language_Name')

@admin.register(LanguageModel)
class LanguageModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'Language_Name', 'Proficiency_Level')
    search_fields = ('user__username', 'Language_Name')

@admin.register(SkillModel)
class SkillModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'Skill_Name', 'Skill_Level')
    search_fields = ('user__username', 'Skill_Name')

@admin.register(IntermediateSkillModel)
class IntermediateSkillModelAdmin(admin.ModelAdmin):
    list_display = ('My_Skill_Name',)
    search_fields = ('My_Skill_Name',)

# Optionally, you can customize the admin panel further with actions, inlines, etc.

