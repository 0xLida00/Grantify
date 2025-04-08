from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'proposals_app'

urlpatterns = [
    path('', views.proposal_list, name='proposal_list'),
    path('<int:pk>/', views.proposal_detail, name='proposal_detail'),
    path('<int:pk>/update/', views.proposal_update, name='proposal_update'),
    path('<int:pk>/delete/', views.proposal_delete, name='proposal_delete'),
    path('admin/', views.admin_proposal_list, name='admin_proposal_list'),
    path('admin/<int:pk>/', views.admin_proposal_detail, name='admin_proposal_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)