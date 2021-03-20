from django.urls import path, include
from . import views

urlpatterns = [
    # path('mails/', views.downloadMails, name='downloadmails'),
    path('boards/', views.downloadLists, name='downloadBoards'),
    path('boards/<slug:board_id>/', views.downloadLists, name='downloadLists'),
    path('filter_mails/', views.filterMails, name='filterMails')

    ]