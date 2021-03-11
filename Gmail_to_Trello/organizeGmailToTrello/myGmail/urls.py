from django.urls import path, include
from . import views

urlpatterns = [
    path('mails/', views.downloadMails, name='download_mails'),

    ]