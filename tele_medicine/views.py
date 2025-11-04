from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from .models import CustomUser


def logout_view(request):
    request.session.flush()
    messages.success(request, 'You have been logged out.')
    return redirect('home')

def navigation(request):
    return render(request, 'tele_medicine/navigation.html')

def diagnosis(request):
    return render(request, 'tele_medicine/Diagnosis.html')

def home(request):
    return render(request, 'tele_medicine/home.html')

def about(request):
    return render(request, 'tele_medicine/about.html')

def services(request):
    return render(request, 'tele_medicine/services.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = CustomUser.objects.get(email=email)
            if user and user.password and check_password(password, user.password):
                # Set up session
                request.session['user_id'] = user.id
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('mainpage')
            else:
                messages.error(request, 'Invalid credentials')
        except CustomUser.DoesNotExist:
            messages.error(request, 'Invalid credentials')
    return render(request, 'tele_medicine/login.html')

def main_page(request):
    return render(request, 'tele_medicine/mainPage.html')

def contact(request):
    return render(request, 'tele_medicine/contact.html')

def signup(request):
    if request.method == 'POST':
        # Collect data safely
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        date_of_birth = request.POST.get('date_of_birth')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        # Basic validation
        if not (first_name and last_name and email and password):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'tele_medicine/signup.html')

        # Hash the password before saving
        hashed_password = make_password(password)

        try:
            user = CustomUser(
                first_name=first_name,
                last_name=last_name,
                email=email,
                date_of_birth=date_of_birth if date_of_birth else None,
                phone_number=phone_number,
                password=hashed_password,
            )
            user.save()
        except IntegrityError:
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'tele_medicine/signup.html')

        messages.success(request, 'Account created successfully. Please log in.')
        return redirect('login')
    return render(request,'tele_medicine/signup.html')