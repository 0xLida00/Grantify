from django.urls import path
from . import views

urlpatterns = [
    path('assign/', views.assign_evaluators, name='assign_evaluators'),
    path('monitor/', views.monitor_evaluations, name='monitor_evaluations'),
    path('evaluation/dashboard/', views.evaluator_dashboard, name='evaluator_dashboard'),
    path('submit/<int:pk>/', views.submit_evaluation, name='submit_evaluation'),
]