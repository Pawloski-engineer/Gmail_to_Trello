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

trello_key = "213abf64ea582c0124da5fcfdb5a6cab"

# def downloadMails(request):
#
#     """Shows basic usage of the Gmail API.
#     Lists the user's Gmail labels.
#     """
#     creds = None
#     # The file token.pickle stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     user = request.user
#     result = SocialToken.objects.filter(account__user=user, account__provider="google")[0]
#     google_token = result.token
#     info = {'client_id':'50255132291-r0p1je5i2il7dte7ko5u78le0r2bd82r.apps.googleusercontent.com', 'client_secret':'9Guzas1mEJK1VXDczxQY_tvT', 'refresh_token': google_token}
#     creds = Credentials.from_authorized_user_info(info) #here
#
#
#
#     result_token = SocialToken.objects.filter(account__user=user, account__provider="trello")[0]
#     result_user = SocialAccount.objects.filter(user=user, provider="trello")[0]
#
#     trello_user_token = result_token.token
#     trello_uid = result_user.uid
#
#     trello_content_json = (requests.get('https://api.trello.com/1/members/' + trello_uid + '/boards?key=' + trello_key + '&token=' +  trello_user_token))
#     trello_content = json.loads(trello_content_json.text)
#
#     service = build('gmail', 'v1', credentials=creds)
#
#     # Get Messages
#     results = service.users().messages().list(userId='me', labelIds='INBOX').execute()
#     messages = results.get('messages', [])
#
#     # message_count = request.data["message_count"] #int(input("How many messages should be displayed?"))
#     message_count = 5
#     if not (message_count > 0):
#         return Response("msg count reqieed")
#
#     if not messages:
#         print('No messages found.')
#     else:
#         print('Messages:')
#         responsemessages = []
#         for message in messages[:message_count]:
#             msg = service.users().messages().get(userId='me', id=message['id']).execute()
#
#             #m = Mail(snippet=msg['snippet'])
#             # m = (msg['id'], msg['snippet'])
#             m = (msg['snippet'])
#             print(m)
#             responsemessages.append(m)
#             # m.save()
#         # return responsemessages
#         # return render(request, 'myGmail/view-mails.html', responsemessages)
#         context = {
#             'responsemessages': responsemessages,
#             'trellocontent': trello_content,
#         }
#
#         return render(request, 'myGmail/view-mails.html', context)
#
# def downloadBoards(request):
#     return downloadLists(request, None)


def downloadLists(request, board_id=None):
    user = request.user
    result_token = SocialToken.objects.filter(account__user=user, account__provider="trello")[0]
    result_user = SocialAccount.objects.filter(user=user, provider="trello")[0]

    trello_user_token = result_token.token
    trello_uid = result_user.uid

    trello_content_json = (requests.get(
        'https://api.trello.com/1/members/' + trello_uid + '/boards?key=' + trello_key + '&token=' + trello_user_token))
    trello_boards = json.loads(trello_content_json.text)

    trello_lists_of_the_board = []
    if board_id:
        trello_list_content_json = (requests.get(
            'https://api.trello.com/1/boards/' + board_id + '/lists?key=' + trello_key + '&token=' + trello_user_token))
        trello_lists_of_the_board = json.loads(trello_list_content_json.text)

    context = {
        'selected_id': board_id,
        'trello_boards': trello_boards,
        'trello_lists': trello_lists_of_the_board,
    }

    return render(request, 'myGmail/view-boards.html', context)

def trello_destination(request):
    form = KeyWordForm(request.POST)
    if form.is_valid():
        key_word = form.cleaned_data.get("key_word")
        board_id = form.cleaned_data.get("board_id")
        list_id = form.cleaned_data.get("list_id")
        # print(key_word, board_id, list_id)
        print(key_word)
        print(board_id)
        print(list_id)

    else:
        print("something is no yes")
        print('errors', form.errors)
    return render(request, 'myGmail/index.html')

