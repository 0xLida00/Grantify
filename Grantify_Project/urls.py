"""
URL configuration for Grantify_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from frontend.views import home

urlpatterns = [
    path("", home, name="home"),
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('accounts/', include('accounts_app.urls')),
    path('calls/', include('calls_app.urls')),
    path('', include('support_app.urls')),
    path('proposals/', include('proposals_app.urls')),
    path('evaluations/', include('evaluation_app.urls')),
    path('alerts/', include('alerts_app.urls')),
    path('reports/', include('reports_app.urls')),
    path('audit/', include('audit_app.urls')),
    path('search/', include('frontend.urls')), 
]