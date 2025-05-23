import json, time, logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator
from .models import FAQ, SupportTicket, Feedback, ToDo
from django.db.models import Q
from .serializers import FAQSerializer, SupportTicketSerializer, FeedbackSerializer, ToDoSerializer
from .forms import SupportTicketForm, FeedbackForm, FAQForm
from django.views import View
from decouple import config

logger = logging.getLogger(__name__)

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


# Support Ticket Create View
class SupportTicketCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SupportTicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "Support ticket created successfully!"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Failed to create support ticket. Please check the form.",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


# Feedback Create View
class FeedbackCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "Feedback submitted successfully!"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "message": "Failed to submit feedback. Please check the form.",
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


@staff_member_required
def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    paginator = Paginator(feedbacks, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'support_app/feedback_list.html', {'page_obj': page_obj})


@staff_member_required
def support_feedback_detail(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    return render(request, 'support_app/feedback_detail.html', {'feedback': feedback})


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
def faq_page(request):
    query = request.GET.get('q', '')
    faqs = FAQ.objects.filter(status='published').order_by('-created_at')

    if query:
        faqs = faqs.filter(
            Q(question__icontains=query) | Q(answer__icontains=query)
        )

    paginator = Paginator(faqs, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'support_app/faq_page.html', {
        'page_obj': page_obj,
        'query': query,
    })


# Admin FAQ Views
@staff_member_required
def admin_faq_list(request):
    faqs = FAQ.objects.all().order_by('-created_at')
    paginator = Paginator(faqs, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'support_app/admin_faq_list.html', {'page_obj': page_obj})


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
        try:
            data = json.loads(request.body)
            vote_type = data.get('vote_type')

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
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    return JsonResponse({'error': 'Invalid request'}, status=400)


# To-Do Views
@login_required
def todo_page(request):
    return render(request, 'support_app/todo.html')


class ToDoPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = 'page_size'
    max_page_size = 20


class ToDoListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logger.info(f"Fetching to-dos for user: {request.user}")
        todos = ToDo.objects.filter(user=request.user).order_by('-created_at')
        paginator = ToDoPagination()
        result_page = paginator.paginate_queryset(todos, request)
        serializer = ToDoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        logger.info(f"Creating a new to-do for user: {request.user}")
        serializer = ToDoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            logger.info(f"To-Do created successfully for user: {request.user}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Error creating to-do: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        todo = get_object_or_404(ToDo, pk=pk, user=request.user)
        serializer = ToDoSerializer(todo)
        return Response(serializer.data)

    def patch(self, request, pk):
        todo = get_object_or_404(ToDo, pk=pk, user=request.user)
        serializer = ToDoSerializer(todo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"To-Do {pk} updated successfully for user {request.user}")
            return Response(serializer.data)
        logger.error(f"Error updating to-do {pk} for user {request.user}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo = get_object_or_404(ToDo, pk=pk, user=request.user)
        todo.delete()
        logger.info(f"To-Do {pk} deleted successfully for user {request.user}")
        return Response({"message": "To-Do item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

@method_decorator(login_required, name='dispatch')
class ToDoDetailHTMLView(View):
    def get(self, request, pk):
        todo = get_object_or_404(ToDo, pk=pk, user=request.user)
        return render(request, 'support_app/todo_detail.html', {'todo': todo})

    def post(self, request, pk):
        todo = get_object_or_404(ToDo, pk=pk, user=request.user)
        title = request.POST.get('title')
        description = request.POST.get('description')
        completed = request.POST.get('completed') == 'true'

        if not title:
            messages.error(request, "Title cannot be empty.")
            return render(request, 'support_app/todo_detail.html', {'todo': todo})

        todo.title = title
        todo.description = description
        todo.completed = completed
        todo.save()

        messages.success(request, "To-Do updated successfully.")
        return redirect('todo_list')