from urllib import request
from django.shortcuts import redirect,render
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from myApp.models import *

from django.templatetags.static import static  # Import the static function


def signupPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type')
        
        if password==confirm_password:
            
            user = Custom_User.objects.create_user(
                username=username,
                password=password,
                email=email,
                user_type=user_type,
                )
  
        messages.success(request, "Account created successfully.")
        return redirect("signinPage")

    return render(request, 'Common/signup.html')


def signinPage(request):

    if request.method == "POST":

        username= request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(username=username, password=password)

        print(user)

        if user:
            login(request,user)
            return redirect("JobFeed")
        else:
            messages.warning(request, "User not found")
            

    return render(request,'Common/login.html')

def logoutPage(request):

    logout(request)

    return redirect('signinPage')

@login_required
def JobFeed(request):
    
    Job=JobModel.objects.all()
    
    context={
        'Job':Job
    }
    
    
    return render(request,"Common/JobFeed.html",context)


def addJobPage(request):
    current_user=request.user
    if current_user.user_type == "recruiter":
        if request.method=="POST":
            job=JobModel()
            job.user=current_user
            job.job_title=request.POST.get("job_title")
            job.company_name=request.POST.get("company_name")
            job.location=request.POST.get("location")
            job.description=request.POST.get("description")
            job.salary=request.POST.get("salary")
            job.employment_type=request.POST.get("employment_type")
            job.posted_date=request.POST.get("application_deadline")
            job.save()
            messages.success(request,"Job Created Successfully")
            
            return redirect("JobFeed")
        return render(request,'myAdmin/addJobPage.html')
    else:
        
        messages.warning(request,"You are not Recruiter")
        
        
def ApplyNow(request,job_title,apply_id):
    
    current_user=request.user
    
    if current_user.user_type == 'jobseeker':
        
        specific_job=JobModel.objects.get(id=apply_id)
        
        already_exists=jobApplyModel.objects.filter(user=current_user,job=specific_job).exists()
        
        context={
            'specific_job':specific_job,
            'already_exists':already_exists
        }   
        if request.method=='POST':
            Full_Name=request.POST.get("Full_Name")
            Work_Experience=request.POST.get("Work_Experience")
            Skills=request.POST.get("Skills")
            Linkedin_URL=request.POST.get("Linkedin_URL")
            Expected_Salary=request.POST.get("Expected_Salary")
            Resume=request.FILES.get("Resume")
            Cover=request.POST.get("Cover")
            
            apply=jobApplyModel(
                user=current_user,
                job=specific_job,
                Resume=Resume,
                Full_Name=Full_Name,
                Work_Experience=Work_Experience,
                Skills=Skills,
                Expected_Salary=Expected_Salary,
                Linkedin_URL=Linkedin_URL,
                Cover=Cover
            )
            apply.save()
            return redirect("JobFeed")
            
        return render(request,"Seeker/applynow.html",context)
    else:
        messages.warning(request,"You are not a Job Seeker")
        
def profilePage(request):
    
    
    return render(request,"Common/profilePage.html")

def createdJob(request):
    
    current_user=request.user
    
    job=JobModel.objects.filter(user=current_user)
    
    context={
        "Job":job
    }
    return render(request,"myAdmin/createdJob.html",context)


def editJob(request,edit_id):
    
    job=JobModel.objects.get(id=edit_id)
    
    current_user=request.user
    if current_user.user_type == "recruiter":
        if request.method=="POST":
            job=JobModel()
            job.id=request.POST.get("job_id")
            job.user=current_user
            job.job_title=request.POST.get("job_title")
            job.company_name=request.POST.get("company_name")
            job.location=request.POST.get("location")
            job.description=request.POST.get("description")
            job.salary=request.POST.get("salary")
            job.employment_type=request.POST.get("employment_type")
            job.posted_date=request.POST.get("application_deadline")
            job.save()
            messages.success(request,"Job Created Successfully")
            
            return redirect("createdJob")
    else:
        
        messages.warning(request,"You are not Recruiter")
    
    context={
        "Job":job
    }
    
    return render(request,"myAdmin/EditJobPage.html",context)


def deleteJob(request,delete_id):
    
    job=JobModel.objects.get(id=delete_id).delete()
    
    return redirect("createdJob")
    
    

        
        
        
        
    
    