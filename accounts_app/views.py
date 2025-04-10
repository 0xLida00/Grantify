from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from alerts_app.models import Notification
from django.urls import reverse_lazy
from audit_app.models import LogEntry
from .forms import CustomSignupForm, ProfileUpdateForm, UserUpdateForm, CustomPasswordChangeForm
from .models import CustomUser


def signup(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)

            LogEntry.objects.create(
                user=user,
                action="User Registered",
                object_repr=str(user),
                change_message=f"User '{user.username}' registered successfully.",
                log_level="INFO",
                source="User",
            )

            Notification.objects.create(
                user=user,
                notification_type="in_app",
                message="Welcome to Grantify! Your account has been successfully created.",
                is_read=False,
            )

            messages.success(request, "Registration successful. Welcome!")
            return redirect('home')
    else:
        form = CustomSignupForm()
    return render(request, 'accounts_app/signup.html', {'form': form})


def user_login(request):
    next_url = request.GET.get('next', '')
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        next_url = request.POST.get('next') or next_url
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            LogEntry.objects.create(
                user=user,
                action="User Logged In",
                object_repr=str(user),
                change_message=f"User '{user.username}' logged in successfully.",
                log_level="INFO",
                source="User",
            )

            messages.success(request, "You have been logged in.")

            if next_url:
                return redirect(next_url)
            return redirect('home')
        else:
            error_message = "Invalid username or password!"

    return render(request, 'accounts_app/login.html', {'next': next_url, 'error_message': error_message})


def user_logout(request):
    if request.user.is_authenticated:
        LogEntry.objects.create(
            user=request.user,
            action="User Logged Out",
            object_repr=str(request.user),
            change_message=f"User '{request.user.username}' logged out successfully.",
            log_level="INFO",
            source="User",
        )

    logout(request)

    messages.success(request, "You have been logged out.")
    return redirect('home')


@login_required
def profile(request, username):
    user_profile = get_object_or_404(CustomUser, username=username)

    if request.user != user_profile:
        messages.error(request, "You are not authorized to view this profile.")
        return redirect('home')

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            LogEntry.objects.create(
                user=request.user,
                action="Profile Updated",
                object_repr=str(request.user),
                change_message=f"User '{request.user.username}' updated their profile.",
                log_level="INFO",
                source="User",
            )

            # Create a notification
            Notification.objects.create(
                user=request.user,
                notification_type="in_app",
                message="Your profile has been updated successfully.",
                is_read=False,
            )

            messages.success(request, "Profile updated successfully.")
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user)

    return render(request, 'accounts_app/profile.html', {
        'u_form': u_form,
        'p_form': p_form,
        'user_profile': user_profile
    })


@login_required
def password_change(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

            LogEntry.objects.create(
                user=request.user,
                action="Password Changed",
                object_repr=str(request.user),
                change_message=f"User '{request.user.username}' changed their password.",
                log_level="INFO",
                source="User",
            )

            Notification.objects.create(
                user=request.user,
                notification_type="in_app",
                message="Your password has been changed successfully.",
                is_read=False,
            )

            messages.success(request, "Your password has been changed successfully.")
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = CustomPasswordChangeForm(user=request.user)
    return render(request, 'accounts_app/password_change.html', {'form': form})


def password_change_done(request):
    return render(request, 'accounts_app/password_change_done.html')