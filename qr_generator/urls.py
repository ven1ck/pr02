from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate, name='generate'),
    path('download/<int:qr_id>/', views.download_qr, name='download'),
    path('history/', views.history, name='history'),
    path('register/', views.register, name='register'),
]