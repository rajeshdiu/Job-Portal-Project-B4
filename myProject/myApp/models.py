from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser

class Custom_User(AbstractUser):
    USER=[
        ('recruiter','Recruiter'),('jobseeker','JobSeeker')
    ]
    user_type=models.CharField(choices=USER,max_length=120)
    profile_pic=models.ImageField(upload_to="media/profile_pic",null=True)
    def __str__(self):
        return self.username
    

class JobModel(models.Model):
    JOB_TYPE_CHOICES=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('temporary', 'Temporary'),
    ]
    user=models.ForeignKey(Custom_User,null=True,blank=True,on_delete=models.CASCADE)
    job_title = models.CharField(max_length=200, null=True, blank=True) 
    company_name = models.CharField(max_length=200, null=True, blank=True) 
    location = models.CharField(max_length=200, null=True, blank=True) 
    description = models.TextField(null=True, blank=True) 
    salary = models.PositiveIntegerField(null=True, blank=True)  
    employment_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES, null=True, blank=True) 
    posted_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    application_deadline = models.DateTimeField(null=True, blank=True) 
    
    def __str__(self):
        return f"{self.job_title} at {self.company_name}"

class jobApplyModel(models.Model):
    
    user=models.ForeignKey(Custom_User,on_delete=models.CASCADE,null=True)
    job=models.ForeignKey(JobModel,on_delete=models.CASCADE,null=True)
    Resume = models.FileField(upload_to="Media/Resume",max_length=200, null=True, blank=True) 
    Cover = models.TextField(null=True, blank=True) 
    Full_Name = models.CharField(max_length=200, null=True, blank=True) 
    Work_Experience = models.CharField(max_length=200, null=True, blank=True) 
    Skills = models.CharField(max_length=200, null=True, blank=True) 
    Linkedin_URL = models.URLField(max_length=200, null=True, blank=True) 
    Expected_Salary = models.PositiveIntegerField( null=True, blank=True) 
    
    
