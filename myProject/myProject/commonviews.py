
from django.shortcuts import redirect,render,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from myApp.models import *
from django.contrib.auth.decorators import login_required
from django.http import Http404

from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash

@login_required
def changePasswordPage(request):
    
    current_user=request.user
    
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        newPassword = request.POST.get('newPassword')
        confirmPassword = request.POST.get('confirmPassword')
        
        if check_password(old_password,request.user.password):
            
            if  newPassword == confirmPassword:
                
                current_user.set_password(newPassword)
                
                current_user.save()
                
                update_session_auth_hash(request,current_user)
                
                messages.success(request, "Password Changed successfully.")
    
    return render(request,"Common/changePasswordPage.html")


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
def createBasicInfo(request):
    if request.user.user_type == 'jobseeker' or request.user.user_type == 'recruiter' :
        current_user = request.user
        
        if request.method == 'POST':
            resume, created = BasicInfoModel.objects.get_or_create(user=current_user)
            
            resume.contact_No = request.POST.get("contact_No")
            resume.Designation = request.POST.get("Designation")
            resume.MySettingsPage_Pic = request.FILES.get("MySettingsPage_Pic")
            resume.Carrer_Summary = request.POST.get("Carrer_Summary")
            resume.Age = request.POST.get("Age")
            resume.Gender = request.POST.get("Gender")
            resume.save()
            
            current_user.first_name = request.POST.get("first_name")
            current_user.last_name = request.POST.get("second_name")
            current_user.save()
            
            messages.success(request, "Resume created successfully.")
            return redirect('MySettingsPage')  
        
        return render(request, "Common/createBasicInfo.html")
    elif request.user.user_type == 'admin':
        messages.warning(request, "You are not authorized to access this page.")
        return render(request, "Common/createBasicInfo.html") 
    
@login_required
def profile_view(request):
    current_user = request.user

    try:
        information = get_object_or_404(BasicInfoModel, user=current_user)
    except Http404:
        messages.warning(request, "You don't have a resume. Please create one.")
        return redirect('createBasicInfo') 

    languages = LanguageModel.objects.filter(user=current_user)
    skills = SkillModel.objects.filter(user=current_user)
    education = EducationModel.objects.filter(user=current_user)
    interests = InterestModel.objects.filter(user=current_user)
    experiences = ExperienceModel.objects.filter(user=current_user)

    context = {
        'Information': information,
        'Languages': languages,
        'Skills': skills,
        'Education': education,
        'Interests': interests,
        'Experiences': experiences,
    }
    
    return render(request, "Common/profilePage.html", context)

    
@login_required
def MySettingsPage(request):
    
    current_user=request.user
    
    myLanguage=LanguageModel.objects.filter(user=current_user)
    mySkill=SkillModel.objects.filter(user=current_user)
    myEducation=EducationModel.objects.filter(user=current_user)
    myInterest=InterestModel.objects.filter(user=current_user)
    myExperience=ExperienceModel.objects.filter(user=current_user)
    
    context={
        "myLanguage":myLanguage,
        "mySkill":mySkill,
        "myInterest":myInterest,
        'myEducation':myEducation,
        "myExperience":myExperience
    }
    
    return render(request,"Common/MySettingsPage.html",context)




