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
    
    STATUS_CHOICES = [
        
        ('pending', 'Pending'),
        ('applied', 'Applied'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]

    user=models.ForeignKey(Custom_User,on_delete=models.CASCADE,null=True)
    job=models.ForeignKey(JobModel,on_delete=models.CASCADE,null=True)
    Resume = models.FileField(upload_to="Media/Resume",max_length=200, null=True, blank=True) 
    Cover = models.TextField(null=True, blank=True) 
    Full_Name = models.CharField(max_length=200, null=True, blank=True) 
    Work_Experience = models.CharField(max_length=200, null=True, blank=True) 
    Skills = models.CharField(max_length=200, null=True, blank=True) 
    Linkedin_URL = models.URLField(max_length=200, null=True, blank=True) 
    Expected_Salary = models.PositiveIntegerField( null=True, blank=True) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    def __str__(self) -> str:
        return self.user.username+"-"+self.job.job_title
    
    
class MessageModel(models.Model):
    application = models.ForeignKey(jobApplyModel, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(Custom_User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(Custom_User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.sender.username+"-"+self.application.Full_Name
    
    
class BasicInfoModel(models.Model):
    user = models.OneToOneField(Custom_User, null=True, on_delete=models.CASCADE)
    contact_No = models.CharField(max_length=100, null=True)
    Designation = models.CharField(max_length=100, null=True)
    Profile_Pic = models.ImageField(upload_to="Media/Profile_Pic", null=True)
    Carrer_Summary = models.CharField(max_length=100, null=True)
    Age = models.PositiveIntegerField(null=True)
    Gender = models.CharField(max_length=100, null=True)
    
    # Date fields
    date_of_birth = models.DateField(null=True, blank=True)
 
    def __str__(self) -> str:
        return self.user.username + " " + self.Designation



class ExperienceModel(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.company_name} ({self.user.username})"


class InterestModel(models.Model):
    user = models.ForeignKey(Custom_User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class FieldOfStudyModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class DegreeModel(models.Model):
    
    Degree=[
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('doctorate', 'Doctorate'),
        ('diploma', 'Diploma'),
        ('certificate', 'Certificate'),
    ]
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=50, choices=Degree)

    def __str__(self):
        return self.name


class InstituteNameModel(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=512, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name
    

class EducationModel(models.Model):
    user = models.ForeignKey(Custom_User, null=True, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=100, null=True)
    degree = models.CharField(max_length=100, null=True)
    field_of_study = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'institution_name', 'degree']

    def __str__(self) -> str:
        return f"{self.user.username} - {self.institution_name} ({self.degree})"



    
class IntermediateLanguageModel(models.Model):
    
    user=models.ForeignKey(Custom_User,null=True,on_delete=models.CASCADE)
    Language_Name=models.CharField(max_length=100,null=True)

    
    def __str__(self) -> str:
        return self.Language_Name  
    
class LanguageModel(models.Model):
    
    Proficiency_Level_Choices=[
        ('beginner','Beginner'),
        ('intermediate','Intermediate'),
        ('expert','Expert'),
    ]

    user=models.ForeignKey(Custom_User,null=True,on_delete=models.CASCADE)
    Language_Name=models.CharField(max_length=100,null=True)
    Proficiency_Level=models.CharField(choices=Proficiency_Level_Choices,max_length=100,null=True)
    
    
    class Meta:
        unique_together=['user','Language_Name']
    
    def __str__(self) -> str:
        return self.user.username+ " "+ self.Language_Name

    

class SkillModel(models.Model):
    
    
    Skill_Level_Choices=[
        ('beginner','Beginner'),
        ('intermediate','Intermediate'),
        ('expert','Expert'),
    ]
    user=models.ForeignKey(Custom_User,null=True,on_delete=models.CASCADE)
    Skill_Name=models.CharField(max_length=100,null=True)
    Skill_Level=models.CharField(choices=Skill_Level_Choices,max_length=100,null=True)
    
    class Meta:
        unique_together=['user','Skill_Name']
    
    def __str__(self) -> str:
        return self.user.username+ " "+ self.Skill_Name
    
class IntermediateSkillModel(models.Model):
    
    My_Skill_Name=models.CharField(max_length=100,null=True)
    
    def __str__(self) -> str:
        return self.My_Skill_Name
    