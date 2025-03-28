from django.urls import path
from . import views

urlpatterns = [
    path('reports/dashboard/', views.dashboard, name='dashboard'),
    path('reports/', views.report_list, name='report_list'),
    path('reports/<int:pk>/', views.report_detail, name='report_detail'),
]