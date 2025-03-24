import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .models import FAQ, SupportTicket, Feedback
from .serializers import FAQSerializer, SupportTicketSerializer, FeedbackSerializer
from .forms import SupportTicketForm, FeedbackForm
from django.views.generic import ListView

openai.api_key = "your_openai_api_key"

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            # Send the user message to OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message},
                ],
            )

            chatbot_message = response["choices"][0]["message"]["content"]
            return JsonResponse({"message": chatbot_message}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=400)

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

# API View for Creating Support Tickets
class SupportTicketCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SupportTicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Support ticket created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API View for Creating Feedback
class FeedbackCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Feedback submitted successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# FAQ Page View
class FAQPageView(ListView):
    model = FAQ
    template_name = "support_app/faq_page.html"
    context_object_name = "faqs"