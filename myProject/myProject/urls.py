
from django.contrib import admin
from django.urls import path
from myProject.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',signupPage,name='signupPage'),
    path('logoutPage/',logoutPage,name='logoutPage'),
    path('signinPage/',signinPage,name='signinPage'),
    path('JobFeed/',JobFeed,name='JobFeed'),
    path('addJobPage/',addJobPage,name='addJobPage'),
    path('ApplyNow/<str:job_title>/<str:apply_id>/',ApplyNow,name='ApplyNow'),
    
    path('ApplyNow/viewMessage/<str:viewMessage_id>',viewMessage,name='viewMessage'),
    path('job/<int:job_id>/application/<int:application_id>/send-message/', send_message, name='send_message'),
    path('job/<int:job_id>/messages/', message_list, name='message_list'),
    path('my-messages/', myMessages, name='my_messages'),
     
    
    
    path('createdJob/',createdJob,name='createdJob'),
    path('appliedJob/',appliedJob,name='appliedJob'),
    path('applicantList/<str:job_id>/',applicantList,name='applicantList'),
    path('editJob/<str:edit_id>/',editJob,name='editJob'),
    path('deleteJob/<str:delete_id>/',deleteJob,name='deleteJob'),
    path('viewJob/<str:view_id>/',viewJob,name='viewJob'),
    
    path('job/<int:job_id>/applicants/<int:application_id>/interview/',callForInterview, name='call_for_interview'),
    path('job/<int:job_id>/applicants/<int:application_id>/reject/',rejectApplication, name='reject_application'),
    
      path('addSkillPage/',addSkillPage,name="addSkillPage"),
    path('createBasicInfo/',createBasicInfo,name="createBasicInfo"),
    path('addLanugage/',addLanugage,name="addLanugage"),
    path('MySettingsPage/',MySettingsPage,name="MySettingsPage"),
    path('addSkillPage/',addSkillPage,name="addSkillPage"),
    path('add_education',add_education,name="add_education"),
    path('add_interest',add_interest,name="add_interest"),
    path('add-experience/', add_experience, name='add_experience'),
    
    
    path('settings/', MySettingsPage, name='MySettingsPage'),
    path('profile_view/', profile_view, name='profile_view'),
    
    
    path('delete_language/<int:id>/', delete_language, name='delete_language'),
    path('delete_skill/<int:id>/', delete_skill, name='delete_skill'),
    path('delete_interest/<int:id>/', delete_interest, name='delete_interest'),
    path('delete_education/<int:id>/', delete_education, name='delete_education'),
    path('delete_experience/<int:id>/', delete_experience, name='delete_experience'),
    
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
