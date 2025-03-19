from django.urls import path
from .views import (
    GrantCallListView,
    GrantCallCreateView,
    GrantCallDetailView,
    GrantCallUpdateView,
    GrantCallDeleteView,
    add_question,
)

urlpatterns = [
    path("", GrantCallListView.as_view(), name="grant_call_list"),  # Use the class-based view
    path("create/", GrantCallCreateView.as_view(), name="grant_call_create"),
    path("<int:pk>/", GrantCallDetailView.as_view(), name="grant_call_detail"),
    path("<int:pk>/update/", GrantCallUpdateView.as_view(), name="grant_call_update"),
    path("<int:pk>/delete/", GrantCallDeleteView.as_view(), name="grant_call_delete"),
    path("<int:grant_call_id>/add-question/", add_question, name="add_question"),
]