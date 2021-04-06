from allauth.socialaccount.models import SocialToken, SocialAccount
from django.contrib.auth.models import User
from google.oauth2.credentials import Credentials

import requests
import json
import csv

from googleapiclient.discovery import build

trello_key = "213abf64ea582c0124da5fcfdb5a6cab"  #TODO put those int settings.py
trello_token = "d1883cff1de9834e7c537dffb70d9dc713441e16b35e53fc8098458a44461c9b"


def download_mails(user_id):  # JavaScript camelCase, Python name_is_like_that

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    user = User.objects.get(id=user_id)

    # result = SocialToken.objects.filter(account__user=user, account__provider="google")[0]
    # google_token = result.token

    account = user.socialaccount_set.get(provider="google")
    refresh_token = account.socialtoken_set.first().token_secret
    google_token = refresh_token

    # put info to settings.py
    info = {'client_id': '50255132291-r0p1je5i2il7dte7ko5u78le0r2bd82r.apps.googleusercontent.com',
            'client_secret': '9Guzas1mEJK1VXDczxQY_tvT', 'refresh_token': google_token}
    creds = Credentials.from_authorized_user_info(info)  # here

    service = build('gmail', 'v1', credentials=creds)

    # Get Messages
    results = service.users().messages().list(userId='me', labelIds='INBOX').execute()
    messages = results.get('messages', [])  # load just some messages, not all

    # message_count = request.data["message_count"] #int(input("How many messages should be displayed?"))
    message_count = 20

    if not messages:
        print('No messages found.')
    else:
        responsemessages = []
        for message in messages[:message_count]:  # i download all mails and then search 20 of downloaded messages TODO change it somehow
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            m = (msg['snippet'])
            responsemessages.append(m)

        return responsemessages


def trello_existing_cards(list_id):
    get_cards_requests = f"https://api.trello.com/1/lists/{list_id}/cards"
    querry = {
        'key': trello_key,
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



def send_mails_to_trello(key_word, list_id, mails):   #TODO add checking list existence - user may delete list from trello
    #mails are downloaded in ecternal function to prevent from downloading them several times
    trello_cards = trello_existing_cards(list_id)
    for mail in mails:
        if mail not in trello_cards and key_word.lower() in mail.lower():
            trello_url = f"https://api.trello.com/1/cards?key={trello_key}&token={trello_token}&idList={list_id}&name={mail}"
            r = requests.post(trello_url)

def change_csv_to_a_list():
    with open('trello_destination.csv', newline='') as csv_file:
        reader = csv.reader(csv_file)
        data = list(reader)
        csv_file.close()
        return data