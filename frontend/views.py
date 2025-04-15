from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from proposals_app.models import Proposal
from support_app.models import SupportTicket, FAQ
from reports_app.models import Report
from support_app.models import ToDo


def home(request):
    dark_mode = request.COOKIES.get('darkMode') == 'enabled'
    return render(request, 'home.html', {'dark_mode': dark_mode})


@login_required
def site_search(request):
    query = request.GET.get('q', '').strip()
    user = request.user
    proposals, tickets, reports, faqs, todos = [], [], [], [], []

    if query:
        proposals = Proposal.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            applicant=user
        )

        tickets = SupportTicket.objects.filter(
            Q(subject__icontains=query) | Q(description__icontains=query),
            user=user
        )

        reports = Report.objects.filter(
            Q(generated_by=user),
            Q(generated_by__username__icontains=query)
        )

        faqs = FAQ.objects.filter(
            Q(question__icontains=query) | Q(answer__icontains=query)
        )

        todos = ToDo.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            user=user
        )

    context = {
        'query': query,
        'proposals': proposals,
        'tickets': tickets,
        'reports': reports,
        'faqs': faqs,
        'todos': todos,
    }
    return render(request, 'site_search.html', context)