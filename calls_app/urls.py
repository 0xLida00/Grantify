from django.urls import path
from .views import (
    GrantCallListView,
    GrantCallCreateView,
    GrantCallDetailView,
    GrantCallUpdateView,
    GrantCallDeleteView,
    add_question,
    toggle_favorite,
    FavoriteGrantCallsView,
    apply_grant_call
)

urlpatterns = [
    path("", GrantCallListView.as_view(), name="grant_call_list"),  # Use the class-based view
    path("create/", GrantCallCreateView.as_view(), name="grant_call_create"),
    path("<int:pk>/", GrantCallDetailView.as_view(), name="grant_call_detail"),
    path("<int:pk>/apply/", apply_grant_call, name="apply_grant_call"),
    path("<int:pk>/toggle-favorite/", toggle_favorite, name="toggle_favorite"),
    path("favorites/", FavoriteGrantCallsView.as_view(), name="favorite_grant_calls"),
    path("<int:pk>/update/", GrantCallUpdateView.as_view(), name="grant_call_update"),
    path("<int:pk>/delete/", GrantCallDeleteView.as_view(), name="grant_call_delete"),
    path("<int:grant_call_id>/add-question/", add_question, name="add_question"),
]