
# To process tasks additionally to py manage.py runserver a command has to be sent:
# python manage.py process_tasks

from allauth.socialaccount.models import SocialToken, SocialAccount
# from allauth.socialaccount.providers.trello.provider import TrelloProvider #in this file there is a problrm with incorrect url
# https://github.com/pennersr/django-allauth/issues/2378
import requests
import json

trello_key = "213abf64ea582c0124da5fcfdb5a6cab"  #TODO put those int settings.py
trello_token = "d1883cff1de9834e7c537dffb70d9dc713441e16b35e53fc8098458a44461c9b"




from .tasks import download_some_mails

from django.shortcuts import render

from .forms import KeyWordForm


def index(request):
    return render(request, 'myGmail/index.html')


def download_lists(request, board_id=None):
    user = request.user
    result_token = SocialToken.objects.filter(account__user=user, account__provider="trello")[0]  # raise exception of no tokens found
    result_user = SocialAccount.objects.filter(user=user, provider="trello")[0]

    trello_user_token = result_token.token
    trello_uid = result_user.uid

    trello_content_json = (requests.get(
        f"https://api.trello.com/1/members/{trello_uid}/boards?key={trello_key}&token={trello_user_token}"))
    trello_boards = json.loads(trello_content_json.text)

    trello_lists_of_the_board = []
    if board_id:
        trello_list_content_json = (requests.get(
            f"https://api.trello.com/1/boards/{board_id}/lists?key={trello_key}&token={trello_user_token}"))
        trello_lists_of_the_board = json.loads(trello_list_content_json.text)  #TODO raise exception of no response or if no boards then create one

    context = {
        'selected_id': board_id,
        'trello_boards': trello_boards,
        'trello_lists': trello_lists_of_the_board,
    }

    return render(request, 'myGmail/view-boards.html', context)


def save_trello_destination(request):  # rename function to indicate what it does TODO come up with some name for destination - it shoulkd describe search rules given by user
    form = KeyWordForm(request.POST)
    if form.is_valid():
        key_word = form.cleaned_data.get("key_word")
        list_id = form.cleaned_data.get("list_id")

        # save data to CSV and pass it to the function that sends mails to trello
        csv_file = open("trello_destination.csv", "a")  #file is created
        csv_file.write(f"{key_word},{list_id}\n")
        csv_file.close()

        return render(request, 'myGmail/index.html')

    else:
        print("something is no yes")
        print('errors', form.errors)
    return render(request, 'myGmail/index.html')


def check_mails(request):
    user_id = request.user.id
    download_some_mails(user_id, repeat=60, repeat_until=None)
    return render(request, 'myGmail/index.html')

# TODO Django_background_tasks

