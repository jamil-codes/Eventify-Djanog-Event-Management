from .models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserLoginForm, UserRegisterForm, ProfileEditForm


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
                return redirect('authentication:profile',  username)
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


def profile(request, username):
    if request.method == 'POST':
        ...
    user = get_object_or_404(User, username=username)
    return render(request, 'authentication/profile.html', {
        'user': user
    })


@login_required
@require_POST
def follow_toggle(request, username):
    target = get_object_or_404(User, username=username)
    if request.user == target:
        return redirect("authentication:profile", username=username)

    if target in request.user.following.all():
        request.user.following.remove(target)
    else:
        request.user.following.add(target)

    return redirect("authentication:profile", username=username)


@login_required
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)

    # Prevent editing someone else’s profile
    if request.user != user:
        messages.error(request, "You cannot edit another user's profile.")
        return redirect('authentication:profile', username=user.username)

    if request.method == "POST":
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your profile has been updated successfully.")
            return redirect('authentication:profile', username=user.username)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'authentication/edit_profile.html', {
        'form': form
    })
