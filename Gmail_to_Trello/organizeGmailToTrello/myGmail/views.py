from django.shortcuts import render

# Create your views here.

from allauth.socialaccount.models import SocialToken, SocialAccount
# from allauth.socialaccount.providers.trello.provider import TrelloProvider #in this file there is a problrm with incorrect url
# https://github.com/pennersr/django-allauth/issues/2378

from googleapiclient.discovery import build

from google.oauth2.credentials import Credentials
from django.shortcuts import render

from .forms import KeyWordForm

import requests
import json

trello_key = "213abf64ea582c0124da5fcfdb5a6cab"     # put those int settings.py
trello_token = "d1883cff1de9834e7c537dffb70d9dc713441e16b35e53fc8098458a44461c9b"

def download_mails(request):     #JavaScript camelCase, Python name_is_like_that

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    user = request.user
    result = SocialToken.objects.filter(account__user=user, account__provider="google")[0]
    google_token = result.token
    # put info to settings.py
    info = {'client_id':'50255132291-r0p1je5i2il7dte7ko5u78le0r2bd82r.apps.googleusercontent.com', 'client_secret':'9Guzas1mEJK1VXDczxQY_tvT', 'refresh_token': google_token}
    creds = Credentials.from_authorized_user_info(info) #here

    service = build('gmail', 'v1', credentials=creds)

    # Get Messages
    results = service.users().messages().list(userId='me', labelIds='INBOX').execute()
    messages = results.get('messages', [])          # load just some messages, not all

    # message_count = request.data["message_count"] #int(input("How many messages should be displayed?"))
    message_count = 20
    if not (message_count > 0):
        return Response("msg count reqieed")

    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        responsemessages = []
        for message in messages[:message_count]:        # i download all mails and then search 20 of downloaded messages
            msg = service.users().messages().get(userId='me', id=message['id']).execute()

            m = (msg['snippet'])
            print(m)
            responsemessages.append(m)

        return responsemessages



def download_lists(request, board_id=None):
    user = request.user
    result_token = SocialToken.objects.filter(account__user=user, account__provider="trello")[0]    # raise exception of no tokens found
    result_user = SocialAccount.objects.filter(user=user, provider="trello")[0]

    trello_user_token = result_token.token
    trello_uid = result_user.uid

    trello_content_json = (requests.get(f"https://api.trello.com/1/members/{trello_uid}/boards?key={trello_key}&token={trello_user_token}"))
    trello_boards = json.loads(trello_content_json.text)

    trello_lists_of_the_board = []
    if board_id:
        trello_list_content_json = (requests.get(f"https://api.trello.com/1/boards/{board_id}/lists?key={trello_key}&token={trello_user_token}"))
        trello_lists_of_the_board = json.loads(trello_list_content_json.text)       # raise exception of no response

    context = {
        'selected_id': board_id,
        'trello_boards': trello_boards,
        'trello_lists': trello_lists_of_the_board,
    }

    return render(request, 'myGmail/view-boards.html', context)

def trello_destination(request):    #rename function to indicate what it does
    form = KeyWordForm(request.POST)
    if form.is_valid():
        key_word = form.cleaned_data.get("key_word")
        # board_id = form.cleaned_data.get("board_id")
        list_id = form.cleaned_data.get("list_id")
        # print(key_word)
        # print(board_id)
        # print(list_id)
        # trello_cards = trello_existing_cards(list_id)

        # mails = download_mails(request)

        send_mails_to_trello(request, key_word, list_id)
        return render(request, 'myGmail/index.html')

    else:
        print("something is no yes")
        print('errors', form.errors)
    return render(request, 'myGmail/index.html')

def trello_existing_cards(list_id):
    get_cards_requests = f"https://api.trello.com/1/lists/{list_id}/cards"
    querry = {
        'key':trello_key,
        'token': trello_token
        }
    response = requests.request(
        "GET",
        get_cards_requests,
        params=querry
    )
    trello_cards = json.loads(response.text)
    trello_card_names = []
    for card in trello_cards:
        trello_card_names.append(card['name'])

    return trello_card_names

def send_mails_to_trello(request, key_word, list_id):
    mails = download_mails(request)
    trello_cards = trello_existing_cards(list_id)
    for mail in mails:
        if mail not in trello_cards and key_word.lower() in mail.lower():
            trello_url = f"https://api.trello.com/1/cards?key={trello_key}&token={trello_token}&idList={list_id}&name={mail}"
            r = requests.post(trello_url)