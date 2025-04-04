from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.proposal_list, name='proposal_list'),
    path('<int:pk>/', views.proposal_detail, name='proposal_detail'),
    path('admin/', views.admin_proposal_list, name='admin_proposal_list'),
    path('admin/<int:pk>/', views.admin_proposal_detail, name='admin_proposal_detail'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)