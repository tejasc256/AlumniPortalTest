from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .forms import SignUpForm, LoginForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def home_view(request):
    return render(request, 'home.html')

def signup_view(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        emails = get_emails()
        usremail = form.cleaned_data.get('email')
        if(usremail in emails):
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Unauthorised Email')
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def login_request(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = User.objects.get(email=email.lower()).username
            user = authenticate(username=username, password=password)
            if(user is not None):
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Email not found')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Backup route for login -- Not used in current code -- it requires username instead of email to login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def changepass_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Please correct error')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepass.html', {'form': form})

def get_emails():
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('apicredentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key('1BOxXUGRsVWEQ9X6HiUr3x9KF7RfEZ0HowQ9IvUBK0Do').sheet1
    emails = sheet.col_values(1)
    return emails
