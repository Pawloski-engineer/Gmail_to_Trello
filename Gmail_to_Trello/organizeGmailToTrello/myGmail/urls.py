from django.urls import path, include
from . import views



urlpatterns = [
    path('index/', views.index, name='index'),
    path('boards/', views.download_lists, name='download_lists'),
    path('boards/<slug:board_id>/', views.download_lists, name='download_lists'),
    path('save_trello_destination/', views.save_trello_destination, name='save_trello_destination'),
    path('check_mails/', views.check_mails, name='check_mails'),

    ]