from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm


# HOME
def home(request):
    return render(request, 'home.html')


# REGISTER
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  
            return redirect('dashboard')  
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


# LOGIN
def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


# LOGOUT
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


# FORGOT PASSWORD
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")

        try:
            user = User.objects.get(email=email)

            return redirect('reset_password', email=user.email)

        except User.DoesNotExist:
            messages.error(request, "No account found with that email address.")

    return render(request, "forgot_password.html")


# RESET PASSWORD
def reset_password(request, email):
    if request.method == 'POST':
        new_password = request.POST.get('password')    
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password', email=email)

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            user = authenticate(username=user.username, password=new_password)
            if user:
                login(request, user)

            return redirect('dashboard')

        except User.DoesNotExist:
            messages.error(request, "User not found.")

    return render(request, 'reset_password.html', {'email': email})


def logging_in(request):
    return render(request, 'logging_in.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def logging_in(request):
    return render(request, 'logging_in.html')


# RESET PASSWORD
def reset_password(request, email):
    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password', email=email)

        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            # Authenticate and login user automatically
            user = authenticate(username=user.username, password=new_password)
            if user:
                login(request, user)
                
                # Redirect to logging in page
                return redirect('logging_in')

            return redirect('dashboard')

        except User.DoesNotExist:
            messages.error(request, "User not found.")

    return render(request, 'reset_password.html', {'email': email})
