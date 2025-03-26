from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.proposal_list, name='proposal_list'),
    path('<int:pk>/', views.proposal_detail, name='proposal_detail'),
    path('create/', views.proposal_create, name='proposal_create'),
    path('<int:pk>/update/', views.proposal_update, name='proposal_update'),
    path('<int:pk>/delete/', views.proposal_delete, name='proposal_delete'),
    path('admin/', views.admin_proposal_list, name='admin_proposal_list'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)