from django.urls import path
from . import views

urlpatterns = [
    path('logs/', views.log_list, name='log_list'),
    path('logs/<int:pk>/', views.log_detail, name='log_detail'),
]