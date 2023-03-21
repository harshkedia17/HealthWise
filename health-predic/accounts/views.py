from django.shortcuts import redirect, render
from django.contrib.auth.models import User ,auth
from datetime import datetime
from django.contrib import messages
from .models import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
# Create your views here.
def signup_patient(request):
    if request.method =='POST':
        if request.POST['username'] and request.POST['email'] and  request.POST['name']  and request.POST['gender'] and request.POST['mobile']and request.POST['password']and request.POST['password1'] :
            username = request.POST['username']
            email = request.POST['email']
            name = request.POST['name']
            # dob = request.POST['dob']
            gender = request.POST['gender']
            image = request.FILES.get('profile_picture')
            mobile_no = request.POST['mobile']
            password =  request.POST.get('password')
            password1 =  request.POST.get('password1')
         
            if password==password1:
                if User.objects.filter(username=username).exists():
                    messages.error(request,'username already taken!!')
                    return redirect('signup_patient')
                elif User.objects.filter(email=email).exists():
                    messages.error(request,'Email already taken')
                    return redirect('signup_patient')
                else:
                    user = User.objects.create_user(username=username,password=password,email=email)
                    user.save()
                    
                    new_patient = Patient(user=user,name=name,gender=gender,mobile_number=mobile_no,profile_pic=image)
                    new_patient.save()
                    
                    messages.success(request, 'Thank you for registering with us.')
                    return redirect('login_patient')
            else:
                messages.error(request,'password not matching, please try again')
                return redirect('signup_patient')
        else:
            messages.error(request,'Please make sure all required fields are filled out correctly')
            return redirect('signup_patient')
    else:
        return render(request,'account/signup.html')
     
                         

def signup_doctor(request):
    if request.method == 'POST':
        if request.POST['username'] and request.POST['email'] and  request.POST['name'] and request.POST['dob'] and request.POST['gender'] and request.POST['address']and request.POST['mobile'] and request.POST['password']and request.POST['password1']  and  request.POST['registration_no'] and  request.POST['year_of_registration'] and  request.POST['qualification'] and  request.POST['Medical_Council'] and  request.POST['specialization']:
            username = request.POST['username']
            email = request.POST['email']
            name = request.POST['name']
            dob = request.POST['dob']
            gender = request.POST['gender']

            year_of_registration =  request.POST['year_of_registration']
            qualification =  request.POST['qualification']
            Medical_Council =  request.POST['Medical_Council']
            specialization =  request.POST['specialization']

            registration_no =  request.POST['registration_no']
            mobile_no = request.POST['mobile']
            password =  request.POST.get('password')
            password1 =  request.POST.get('password1')
            if password==password1:
                if User.objects.filter(username=username).exists():
                    messages.error(request,'username already taken!!')
                    return redirect('signup_doctor')
                elif User.objects.filter(email=email).exists():
                    messages.error(request,'Email already taken')
                    return redirect('signup_doctor')
                else:
                    user = User.objects.create_user(username=username,password=password,email=email)
                    user.save()
                    new_doctor = Doctor(user=user,email=email,name=name,dob=dob,gender=gender,year_of_registration=year_of_registration,qualification=qualification,Medical_Council=Medical_Council,specialization=specialization,registration_no=registration_no,mobile_no=mobile_no)
                    new_doctor.save()
                    messages.success(request, 'Thank you for registering with us.')  
                    return redirect('login_doctor')
            else:
                messages.error(request,'password not matching, please try again')
                return redirect('signup_doctor')
        else:
            messages.error(request,'Please make sure all required fields are filled out correctly')
            return redirect('signup_doctor')
    else:
        return render(request,'account/sign_up_doc.html')

            
            

def login_patient(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            try:
                if(user.Patient.is_patient==True):
                    auth.login(request,user)
                    return redirect('home')
            except:
                messages.error(request,'Invalid Credentials')
                return redirect('login_patient')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login_patient')
    else:
        return render(request,'account/login.html')

def login_doctor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            try:
                if(user.Doctor.is_patient==True):
                    auth.login(request,user)
                    return redirect('doctor_dashboard')
            except:
                messages.error(request,'Invalid Credentials')
                return redirect('doctor_login')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('doctor_login')
    else:
        return render(request,'account/sl.html')

@login_required(login_url='login_patient')
def logout(request):
    auth.logout(request)
    messages.success(request,'You have successfully logged out')
    return redirect('patient_login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Patient._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Patient.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('patient_login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('patient_signup')