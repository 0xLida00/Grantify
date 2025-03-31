from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification, NotificationPreference
from .forms import NotificationPreferenceForm

# Display notifications
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'alerts_app/notification_list.html', {'notifications': notifications})

# Mark a notification as read
@login_required
def mark_notification_as_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.mark_as_read()

    messages.success(request, "Notification marked as read.")
    return redirect('notification_list')

# Manage notification preferences
@login_required
def notification_preferences(request):
    preferences, created = NotificationPreference.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = NotificationPreferenceForm(request.POST, instance=preferences)
        if form.is_valid():
            form.save()

            messages.success(request, "Notification preferences updated successfully.")
            return redirect('notification_preferences')
    else:
        form = NotificationPreferenceForm(instance=preferences)
    return render(request, 'alerts_app/notification_preferences.html', {'form': form})