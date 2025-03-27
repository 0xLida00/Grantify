from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('mark-as-read/<int:pk>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('preferences/', views.notification_preferences, name='notification_preferences'),
]