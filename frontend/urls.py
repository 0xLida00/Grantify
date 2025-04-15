from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="frontend_home"),
    path('search/', views.site_search, name='site_search'),
]