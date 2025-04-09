from rest_framework import serializers
from .models import FAQ, SupportTicket, Feedback, ToDo

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'created_at']

class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['id', 'user', 'subject', 'description', 'priority', 'status', 'created_at', 'updated_at']
        read_only_fields = ['user']
class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'message', 'created_at']
        read_only_fields = ['user']

class ToDoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ToDo
        fields = ['id', 'user', 'title', 'description', 'completed', 'due_date', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']