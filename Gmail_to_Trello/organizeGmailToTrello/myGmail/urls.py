from django.urls import path, include
from . import views

urlpatterns = [
    # path('mails/', views.download_mails, name='downloadmails'),
    path('boards/', views.download_lists, name='download_lists'),
    path('boards/<slug:board_id>/', views.download_lists, name='download_lists'),
    path('save_trello_destination/', views.save_trello_destination, name='save_trello_destination'),
    # path('send_mails_to_trello/', views.send_mails_to_trello, name='send_mails_to_trello'),
    # path('change_csv_to_a_list/', views.change_csv_to_a_list, name='change_csv_to_a_list'),
    path('check_mails/', views.check_mails, name='check_mails'),

    # path('mails/', views.downloadMails, name='download_mails')

    ]