import json, time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import FAQ, SupportTicket, Feedback
from .serializers import FAQSerializer, SupportTicketSerializer, FeedbackSerializer
from .forms import SupportTicketForm, FeedbackForm, FAQForm
from django.views.generic import ListView
from decouple import config


# Support Center View
def support_center(request):
    support_ticket_form = SupportTicketForm()
    feedback_form = FeedbackForm()

    return render(request, 'base.html', {
        'support_ticket_form': support_ticket_form,
        'feedback_form': feedback_form,
    })

# API View for FAQs
class FAQListView(APIView):
    def get(self, request):
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data)

class SupportTicketCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SupportTicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "Support ticket created successfully!".strip()},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Failed to create support ticket. Please check the form.".strip(),
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

# API View for Creating Feedback
class FeedbackCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "Feedback submitted successfully!".strip()},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Failed to submit feedback. Please check the form.".strip(),
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

# Admin Ticket List View
@staff_member_required
def admin_ticket_list(request):
    tickets = SupportTicket.objects.all().order_by('-created_at')

    paginator = Paginator(tickets, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        status = request.POST.get('status')
        response = request.POST.get('response')

        ticket = get_object_or_404(SupportTicket, id=ticket_id)
        ticket.status = status
        ticket.response = response
        ticket.save()

        messages.success(request, f"Ticket '{ticket.subject}' updated successfully.")
        return redirect('admin_ticket_list')

    return render(request, 'support_app/admin_ticket_list.html', {'page_obj': page_obj})

# Admin Ticket Detail View
@staff_member_required
def admin_ticket_detail(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id)

    if request.method == 'POST':
        admin_response = request.POST.get('admin_response')

        if ticket.response:
            ticket.response += f"\n\nAdmin Response:\n{admin_response}"
        else:
            ticket.response = f"Admin Response:\n{admin_response}"

        status = request.POST.get('status')
        if status:
            ticket.status = status

        ticket.save()

        messages.success(request, "Your response has been sent successfully.")
        return redirect('admin_ticket_detail', ticket_id=ticket.id)

    return render(request, 'support_app/admin_ticket_detail.html', {'ticket': ticket})

# User Ticket List View
@login_required
def user_ticket_list(request):
    tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')

    paginator = Paginator(tickets, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'support_app/user_ticket_list.html', {'page_obj': page_obj})

# User Ticket Detail View
@login_required
def user_ticket_detail(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)

    if request.method == 'POST':
        user_response = request.POST.get('user_response')

        if ticket.response:
            ticket.response += f"\n\nUser Update:\n{user_response}"
        else:
            ticket.response = f"User Update:\n{user_response}"

        ticket.save()

        messages.success(request, "Your response has been sent successfully.")
        return redirect('user_ticket_detail', ticket_id=ticket.id)

    return render(request, 'support_app/user_ticket_detail.html', {'ticket': ticket})

# FAQ Page View
class FAQPageView(ListView):
    model = FAQ
    template_name = "support_app/faq_page.html"
    context_object_name = "faqs"

    def get_queryset(self):
        return FAQ.objects.filter(status='published').order_by('-created_at')
    
# Admin FAQ List View
@staff_member_required
def admin_faq_list(request):
    faqs = FAQ.objects.all().order_by('-created_at')
    return render(request, 'support_app/admin_faq_list.html', {'faqs': faqs})

# Admin FAQ Create View
@staff_member_required
def admin_faq_create(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "FAQ created successfully.")
            return redirect('admin_faq_list')
    else:
        form = FAQForm()
    return render(request, 'support_app/admin_faq_form.html', {'form': form})

# Admin FAQ Edit View
@staff_member_required
def admin_faq_edit(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            messages.success(request, "FAQ updated successfully.")
            return redirect('admin_faq_list')
    else:
        form = FAQForm(instance=faq)
    return render(request, 'support_app/admin_faq_form.html', {'form': form})

# Admin FAQ Delete View
@staff_member_required
def admin_faq_delete(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    faq.delete()
    messages.success(request, "FAQ deleted successfully.")
    return redirect('admin_faq_list')

# Vote FAQ View
@login_required
@csrf_exempt
def vote_faq(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    user = request.user

    if request.method == 'POST':
        vote_type = request.POST.get('vote_type')

        if vote_type == 'up':
            if user in faq.voted_down.all():
                faq.voted_down.remove(user)
                faq.thumbs_down -= 1

            if user not in faq.voted_up.all():
                faq.voted_up.add(user)
                faq.thumbs_up += 1

        elif vote_type == 'down':
            if user in faq.voted_up.all():
                faq.voted_up.remove(user)
                faq.thumbs_up -= 1

            if user not in faq.voted_down.all():
                faq.voted_down.add(user)
                faq.thumbs_down += 1

        faq.save()
        return JsonResponse({'thumbs_up': faq.thumbs_up, 'thumbs_down': faq.thumbs_down})

    return JsonResponse({'error': 'Invalid request'}, status=400)