from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import LogEntry

# View to display a list of logs
@staff_member_required
def log_list(request):
    logs = LogEntry.objects.all().order_by('-created_at')

    log_level = request.GET.get('log_level')
    if log_level:
        logs = logs.filter(log_level=log_level)

    user_id = request.GET.get('user')
    if user_id:
        logs = logs.filter(user_id=user_id)

    paginator = Paginator(logs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'audit_app/log_list.html', {'page_obj': page_obj})

# View to display details of a specific log entry
@staff_member_required
def log_detail(request, pk):
    log = get_object_or_404(LogEntry, pk=pk)
    return render(request, 'audit_app/log_detail.html', {'log': log})