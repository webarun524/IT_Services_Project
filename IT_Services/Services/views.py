from django.shortcuts import render, redirect, HttpResponse
from Services.models import Service
from Services.forms import RegistrationForm, serviceForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import random
from django.core.mail import send_mail
from django.core.exceptions import ValidationError

# Create your views here.

@login_required(login_url='login')
def index(request):
    obj = Service.objects.all()
    return render(request, 'homeService.html', {'form': obj})

def create(request):
    if request.method == 'POST':
        form = serviceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('read')
        else:
            print(form.errors)
    else:
        form = serviceForm()
    return render(request, 'create.html', {'form': form})


def update(request, id):
    obj = Service.objects.get(id=id)
    if request.method == 'POST':
        form = serviceForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('read')
    else:
        form = serviceForm(instance=obj)
        
    return render(request, 'update.html', {'form': form})

def delete(request, id):
    obj = Service.objects.get(id=id)
    if obj.delete():
        return redirect('read')
    return render(request, 'delete.html')

### Authentication views 

@login_required(login_url='login')
def login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=uname, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('read')
        else:
            return HttpResponse('Your Username and password is incorrect !!!')
    return render(request, 'authenticate/login.html')

def register(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')

        # Check if passwords match
        if pass1 != pass2:
            return HttpResponse('Your password and confirm password are not the same !!!')

        # Check if the username already exists
        if User.objects.filter(username=uname).exists():
            return HttpResponse('Username already exists. Please choose a different username.')

        # Check if the email already exists
        if User.objects.filter(email=email).exists():
            return HttpResponse('Email already in use. Please choose a different email.')

        try:
            # Create new user
            my_user = User.objects.create_user(username=uname, email=email, password=pass1)
            my_user.save()

            # Generate OTP
            otp = random.randint(1000, 9999)
            request.session['otp'] = otp
            request.session['otp_email'] = email

            # Send OTP email
            try:
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is {otp}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                print(f"Sent OTP to {email}: {otp}")  
            except Exception as e:
                print(f"Error sending email: {e}") 
                return render(request, 'authenticate/sigup.html', {'error': f'Error sending email: {e}'})

            return redirect('verify')
        except ValidationError as e:
            return HttpResponse(f'Error: {e}')

    return render(request, 'authenticate/sigup.html')

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        if otp and int(otp) == session_otp:
            del request.session['otp']
            del request.session['otp_email']
            return redirect('login')
        else:
            return render(request, 'authenticate/verify_otp.html', {'error': 'Invalid OTP'})
    
    return render(request, 'authenticate/verify_otp.html')

def logout(request):
    auth_logout(request)
    return redirect('login')
