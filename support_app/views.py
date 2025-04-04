import json, time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from django.contrib import messages
from .models import FAQ, SupportTicket, Feedback
from .serializers import FAQSerializer, SupportTicketSerializer, FeedbackSerializer
from .forms import SupportTicketForm, FeedbackForm
from django.views.generic import ListView
from decouple import config


# Support Center View
def support_center(request):
    # Initialize the forms
    support_ticket_form = SupportTicketForm()
    feedback_form = FeedbackForm()

    # Pass the forms to the base.html template
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
            # Return the success message in the JSON response
            return Response(
                {"message": "Support ticket created successfully!".strip()},
                status=status.HTTP_201_CREATED
            )
        # Return the error message in the JSON response
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
            # Return the success message in the JSON response
            return Response(
                {"message": "Feedback submitted successfully!".strip()},
                status=status.HTTP_201_CREATED
            )
        # Return the error message in the JSON response
        return Response(
            {
                "message": "Failed to submit feedback. Please check the form.".strip(),
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

# FAQ Page View
class FAQPageView(ListView):
    model = FAQ
    template_name = "support_app/faq_page.html"
    context_object_name = "faqs"