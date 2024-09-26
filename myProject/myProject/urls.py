
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
    path('profilePage/',profilePage,name='profilePage'),
    path('createdJob/',createdJob,name='createdJob'),
    
    
    path('editJob/<str:edit_id>/',editJob,name='editJob'),
    path('deleteJob/<str:delete_id>/',deleteJob,name='deleteJob'),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
