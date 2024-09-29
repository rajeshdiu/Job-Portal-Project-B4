from urllib import request
from django.shortcuts import redirect,render,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.hashers import make_password

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import IntegrityError
from django.http import Http404

from django.db.models import Q 

from myApp.models import *

from django.templatetags.static import static  # Import the static function


def searchJob(request):
    
    query = request.GET.get('query')
    
    if query:
        
        jobs = JobModel.objects.filter(Q(job_title__icontains=query) 
                                       |Q(description__icontains=query) 
                                       |Q(employment_type__icontains=query) 
                                       |Q(company_name__icontains=query))
    
    else:
        jobs = JobModel.objects.none()
        
    context={
        'jobs':jobs,
        'query':query
    }
    
    return render(request,"Common/search.html",context)


@login_required
def JobFeed(request):
    
    Job=JobModel.objects.all()
    
    context={
        'Job':Job
    }
    
    
    return render(request,"Common/JobFeed.html",context)

@login_required
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
        
@login_required      
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
                Cover=Cover,
                status="pending"
            )
            apply.save()
            return redirect("JobFeed")
            
        return render(request,"Seeker/applynow.html",context)
    else:
        messages.warning(request,"You are not a Job Seeker")


@login_required
def createdJob(request):
    
    current_user=request.user
    
    job=JobModel.objects.filter(user=current_user)
    
    context={
        "Job":job
    }
    return render(request,"myAdmin/createdJob.html",context)

@login_required
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

@login_required
def deleteJob(request,delete_id):
    
    job=JobModel.objects.get(id=delete_id).delete()
    
    return redirect("createdJob")

@login_required
def viewJob(request,view_id):
    
    job=JobModel.objects.get(id=view_id)
    
    context={
        "job":job
    }
    
    return render(request,"Common/viewJob.html",context)

@login_required
def applicantList(request,job_id):
    
    job = get_object_or_404(JobModel, id=job_id)
    
    applications = jobApplyModel.objects.filter(job=job)

    context = {
        'job': job,
        'applications': applications
    }
    
    return render(request,"myAdmin/applicantList.html",context)

@login_required
def callForInterview(request, job_id, application_id):
    application = get_object_or_404(jobApplyModel, id=application_id)

    application.status = 'interview_scheduled'  
    application.save()

    messages.success(request, 'The applicant has been called for an interview.')
    return redirect('applicantList', job_id=job_id)

@login_required
def rejectApplication(request, job_id, application_id):
    application = get_object_or_404(jobApplyModel, id=application_id)

    # Reject the application
    application.status = 'rejected'  
    application.save()

    messages.success(request, 'The application has been rejected.')

    application_messages = MessageModel.objects.filter(application=application)

    context = {
        'job_id': job_id,
        'application': application,
        'messages': application_messages
    }

    return redirect('applicantList', job_id=job_id)

@login_required
def message_list(request, job_id):
    job = get_object_or_404(JobModel, id=job_id)
    messages = MessageModel.objects.filter(application__job=job)

    context = {
        'job': job,
        'messages': messages
    }
    
    return render(request, 'myAdmin/message_list.html', context)

@login_required
def send_message(request, job_id, application_id):
    current_user = request.user
    job = get_object_or_404(JobModel, id=job_id)
    application = get_object_or_404(jobApplyModel, id=application_id)

    context = {
        'job': job,
        'application': application
    }

    if request.method == 'POST':
        content = request.POST.get('messageText')
        recipient = application.user

        # Check for duplicate messages
        if MessageModel.objects.filter(
            application=application,
            sender=current_user,
            content=content,
            timestamp__gte=timezone.now() - timezone.timedelta(minutes=1)  # Check if sent within the last minute
        ).exists():
            messages.error(request, 'You have already sent this message. Duplicate messages are not allowed.')
            return redirect('message_list', job_id=job_id)

        # If no duplicate, save the message
        message = MessageModel(
            application=application,
            sender=current_user,
            recipient=recipient,
            content=content,
            timestamp=timezone.now()
        )
        message.save()

        messages.success(request, 'Message sent successfully!')
        return redirect('message_list', job_id=job_id)

    else:
        return render(request, 'myAdmin/send_message.html', context)


@login_required
def viewMessage(request, viewMessage_id):
    application = get_object_or_404(jobApplyModel, id=viewMessage_id)
    
    messages = MessageModel.objects.filter(application=application).order_by('timestamp')
    
    context={
        'application': application,
        'messages': messages
    }
    
    return render(request, "Seeker/viewMessage.html",context )

@login_required
def appliedJob(request):
    current_user = request.user

    # Get all job applications for the current user
    job_applications = jobApplyModel.objects.filter(user=current_user)

    job_messages = {}
    for job_application in job_applications:
        messages = MessageModel.objects.filter(application=job_application)
        job_messages[job_application.id] = messages

    context = {
        "Job": job_applications,
        "job_messages": job_messages, 
    }
    return render(request, "Seeker/appliedJob.html", context)

@login_required
def myMessages(request):
    # Get all messages where the logged-in user is the recipient
    messages = MessageModel.objects.filter(recipient=request.user).order_by('-timestamp')

    # Create a set to hold job applications linked to the messages
    applications = set()

    for message in messages:
        applications.add(message.application)

    # Check if any applications have been rejected or selected for interview
    rejected_apps = [app for app in applications if app.status == 'rejected']
    selected_apps = [app for app in applications if app.status == 'interview_scheduled']  # Change this as per your interview status

    context = {
        'messages': messages,
        'rejected_apps': rejected_apps,  # Pass the rejected applications to the context
        'interviewed_apps': selected_apps,  # Pass the selected applications to the context
    }
    return render(request, 'Common/myMessages.html', context)
@login_required
def addLanugage(request):
    # Check if the user is a viewer
    if request.user.user_type != 'jobseeker':
        messages.warning(request, "You are not authorized to add languages.")
        return redirect('MySettingsPage')  # Redirect to an appropriate page

    all_lan = IntermediateLanguageModel.objects.all()
    current_user = request.user

    if request.method == 'POST':
        Language_Id = request.POST.get("Language_Id")
        Proficiency_Level = request.POST.get("Proficiency_Level")

        # Validate the input
        if not Language_Id or not Proficiency_Level:
            messages.warning(request, "Both language and proficiency level are required.")
            return render(request, "myAdmin/addLanguage.html", {'all_lan': all_lan})

        MyObj = get_object_or_404(IntermediateLanguageModel, id=Language_Id)

        if LanguageModel.objects.filter(user=current_user, Language_Name=MyObj.Language_Name).exists():
            messages.warning(request, "This language already exists in your MySettingsPage.")
            return render(request, "myAdmin/addLanguage.html", {'all_lan': all_lan})

        LanguageModel.objects.create(
            user=current_user,
            Language_Name=MyObj.Language_Name,
            Proficiency_Level=Proficiency_Level,
        )
        messages.success(request, "Language added successfully.")
        return redirect("MySettingsPage")

    context = {
        "all_lan": all_lan
    }
    return render(request, "myAdmin/addLanguage.html", context)



@login_required
def addSkillPage(request):
    # Check if the user is a viewer
    if request.user.user_type != 'jobseeker':
        messages.warning(request, "You are not authorized to add skills.")
        return redirect('MySettingsPage')  # Redirect to an appropriate page

    All_Skill = IntermediateSkillModel.objects.all()
    current_user = request.user

    if request.method == 'POST':
        Skill_Id = request.POST.get("Skill_Id")
        Skill_Level = request.POST.get("Skill_Level")

        MyObj = get_object_or_404(IntermediateSkillModel, id=Skill_Id)

        # Check if the skill already exists for the user
        if SkillModel.objects.filter(user=current_user, Skill_Name=MyObj.My_Skill_Name).exists():
            messages.warning(request, "Skill already exists.")
        else:
            skill = SkillModel(
                user=current_user,
                Skill_Name=MyObj.My_Skill_Name,
                Skill_Level=Skill_Level,
            )
            skill.save()
            messages.success(request, "Skill added successfully.")
            return redirect("MySettingsPage")

    context = {
        "All_Skill": All_Skill
    }

    return render(request, "myAdmin/addSkill.html", context)


@login_required
def add_education(request):
    # Check if the user is a viewer
    if request.user.user_type != 'jobseeker':
        messages.warning(request, "You are not authorized to add education information.")
        return redirect('MySettingsPage')  # Redirect to an appropriate page

    institutes = InstituteNameModel.objects.all()  # Get all institutes
    degrees = DegreeModel.objects.all()  # Get all degrees
    fields_of_study = FieldOfStudyModel.objects.all()  # Get all fields of study

    if request.method == 'POST':
        institution_name = request.POST.get('institution_name')
        degree_name = request.POST.get('degree_name')
        field_of_study_name = request.POST.get('field_of_study')  # Get field of study from dropdown
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Create and save the new education entry
        EducationModel.objects.create(
            user=request.user,  # Assuming the user is logged in
            institution_name=institution_name,
            degree=degree_name,
            field_of_study=field_of_study_name,
            start_date=start_date,
            end_date=end_date
        )
        messages.success(request, "Education added successfully.")
        return redirect('MySettingsPage')  # Redirect to a success page or another view
    
    context={
        'institutes': institutes,
        'degrees': degrees,
        'fields_of_study': fields_of_study
    }

    return render(request, 'myAdmin/addEducation.html', context)


@login_required
def add_interest(request):
    # Check if the user is a viewer
    if request.user.user_type != 'jobseeker':
        messages.warning(request, "You are not authorized to add interests.")
        return redirect('MySettingsPage')  # Redirect to an appropriate page

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        # Validate the input
        if not name or not description:
            messages.warning(request, "Both name and description are required.")
            return render(request, 'add_interest.html')

        InterestModel.objects.create(
            user=request.user, 
            name=name,
            description=description
        )
        messages.success(request, "Interest added successfully.")
        return redirect('MySettingsPage')

    return render(request, 'myAdmin/addInterest.html')


@login_required
def add_experience(request):
    # Check if the user is a viewer
    if request.user.user_type != 'jobseeker':
        messages.warning(request, "You are not authorized to add experience.")
        return redirect('MySettingsPage')  # Redirect to an appropriate page

    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        company_name = request.POST.get('company_name')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')

        # Validate the input
        if not job_title or not company_name or not start_date:
            messages.warning(request, "Job title, company name, and start date are required.")
            return render(request, 'add_experience.html')

        # Create and save the new experience entry
        ExperienceModel.objects.create(
            user=request.user,
            job_title=job_title,
            company_name=company_name,
            start_date=start_date,
            end_date=end_date,
            description=description
        )
        messages.success(request, "Experience added successfully.")
        return redirect('MySettingsPage')  # Redirect to your desired URL

    return render(request, 'myAdmin/addExperience.html')

@login_required
def delete_language(request, id):
    language = get_object_or_404(LanguageModel, id=id)
    language.delete()
    messages.success(request, "Language deleted successfully.")
    return redirect('MySettingsPage')  # Replace with your actual MySettingsPage URL name

@login_required
def delete_skill(request, id):
    skill = get_object_or_404(SkillModel, id=id)
    skill.delete()
    messages.success(request, "Skill deleted successfully.")
    return redirect('MySettingsPage')

@login_required
def delete_interest(request, id):
    interest = get_object_or_404(InterestModel, id=id)
    interest.delete()
    messages.success(request, "Interest deleted successfully.")
    return redirect('MySettingsPage')

@login_required
def delete_education(request, id):
    education = get_object_or_404(EducationModel, id=id)
    education.delete()
    messages.success(request, "Education deleted successfully.")
    return redirect('MySettingsPage')

@login_required
def delete_experience(request, id):
    experience = get_object_or_404(ExperienceModel, id=id)
    experience.delete()
    messages.success(request, "Experience deleted successfully.")
    return redirect('MySettingsPage')



