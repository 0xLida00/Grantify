from django.urls import path
from .views import (
    FAQListView,
    SupportTicketCreateView,
    FeedbackCreateView,
    FAQPageView,
    support_center,
)

urlpatterns = [
    path('api/faqs/', FAQListView.as_view(), name='faq_list'),
    path('api/support-tickets/', SupportTicketCreateView.as_view(), name='support_ticket_create'),
    path('api/feedback/', FeedbackCreateView.as_view(), name='feedback_create'),
    path('faqs/', FAQPageView.as_view(), name='faq_page'),
    path('support-center/', support_center, name='support_center'),
]