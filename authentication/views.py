from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm


def login_view(request):
    form = UserLoginForm()
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if (form.is_valid()):
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('authentication:login')
        else:
            messages.error(
                request, 'Invalid username or password. Please try again.')

    return render(request, 'authentication/login.html', {
        'form': form
    })


def register_view(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if (form.is_valid()):
            user = form.save()
            if user is not None:
                login(request, user)
                messages.success(
                    request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('authentication:login')
        else:
            messages.error(
                request, 'Please Fill All The Fields Correctly.')

    return render(request, 'authentication/register.html', {
        'form': form
    })


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('authentication:login')
