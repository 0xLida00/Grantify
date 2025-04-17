from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from alerts_app.models import Notification, NotificationPreference
from alerts_app.forms import NotificationPreferenceForm


# Display notifications
@login_required
def notification_list(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    paginator = Paginator(notifications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'alerts_app/notification_list.html', {'page_obj': page_obj})


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