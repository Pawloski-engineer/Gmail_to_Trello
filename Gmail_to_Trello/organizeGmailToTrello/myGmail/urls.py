from django.urls import path, include
from . import views

urlpatterns = [
    # path('mails/', views.downloadMails, name='downloadmails'),
    path('boards/', views.downloadLists, name='downloadBoards'),
    path('boards/<slug:board_id>/', views.downloadLists, name='downloadLists'),
    path('trello_destination/', views.trello_destination, name='trello_destination'),
    # path('mails/', views.downloadMails, name='download_mails')

    ]