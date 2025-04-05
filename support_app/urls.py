from django.urls import path
from .views import (
    FAQListView,
    SupportTicketCreateView,
    FeedbackCreateView,
    support_center,
    admin_ticket_list,
    user_ticket_list,
    admin_ticket_detail,
    user_ticket_detail,
    FAQPageView,
    admin_faq_list,
    admin_faq_create,
    admin_faq_edit,
    admin_faq_delete,
    vote_faq,
)

urlpatterns = [
    path('api/faqs/', FAQListView.as_view(), name='faq_list'),
    path('api/support-tickets/', SupportTicketCreateView.as_view(), name='support_ticket_create'),
    path('api/feedback/', FeedbackCreateView.as_view(), name='feedback_create'),
    path('support-center/', support_center, name='support_center'),
    path('admin-panel/tickets/', admin_ticket_list, name='admin_ticket_list'),
    path('admin-panel/tickets/<int:ticket_id>/', admin_ticket_detail, name='admin_ticket_detail'),
    path('user/tickets/', user_ticket_list, name='user_ticket_list'),
    path('user/tickets/<int:ticket_id>/', user_ticket_detail, name='user_ticket_detail'),
    path('faqs/', FAQPageView.as_view(), name='faq_page'),
    path('admin-panel/faqs/', admin_faq_list, name='admin_faq_list'),
    path('admin-panel/faqs/create/', admin_faq_create, name='admin_faq_create'),
    path('admin-panel/faqs/<int:faq_id>/edit/', admin_faq_edit, name='admin_faq_edit'),
    path('admin-panel/faqs/<int:faq_id>/delete/', admin_faq_delete, name='admin_faq_delete'),
    path('faqs/<int:faq_id>/vote/', vote_faq, name='vote_faq'),
]