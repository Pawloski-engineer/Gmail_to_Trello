from django.urls import path, include
from . import views

urlpatterns = [
    # path('mails/', views.download_mails, name='downloadmails'),
    path('boards/', views.download_lists, name='download_lists'),
    path('boards/<slug:board_id>/', views.download_lists, name='download_lists'),
    path('save_trello_destination/', views.save_trello_destination, name='save_trello_destination'),
    # path('mails/', views.downloadMails, name='download_mails')

    ]