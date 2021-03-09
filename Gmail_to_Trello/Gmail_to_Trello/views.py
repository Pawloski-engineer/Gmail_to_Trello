from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import MailSerializer

from .models import Mail

# imports that are used for getting mails from Gmail
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from trello import TrelloClient

@api_view(['GET'])      #@api_view(['GET', 'POST'])
def apiOverview(request):
    api_urls = {
        'List':'/mail-list/',



    }
    return Response(api_urls)

@api_view(['GET'])
def mailList(request):
    mails = Mail.objects.all()
    serializer = MailSerializer(mails, many=True)
    return Response(serializer.data)


# Gmail functions:
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


@api_view(['POST'])
def downloadMails(request):

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Get Messages
    results = service.users().messages().list(userId='me', labelIds='INBOX').execute()
    messages = results.get('messages', [])

    message_count = request.data["message_count"] #int(input("How many messages should be displayed?"))
    if not (message_count > 0):
        return Response("msg count reqieed")

    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        responsemessages = []
        for message in messages[:message_count]:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()

            #m = Mail(snippet=msg['snippet'])
            m = ( msg['id'], msg['snippet'])

            print(m)
            responsemessages.append(m)
            # m.save()
        return Response(responsemessages)

@api_view(['GET'])
def trelloBoards(request):
    client = TrelloClient(
        api_key='213abf64ea582c0124da5fcfdb5a6cab',
        token='d1883cff1de9834e7c537dffb70d9dc713441e16b35e53fc8098458a44461c9b',
    )
    all_boards = client.list_boards()
    boards = []
    for entry in all_boards:
        boards.append((entry.id, entry.name))

    return Response(boards)

@api_view(['GET'])
def trelloLists(request):
    client = TrelloClient(
        api_key='213abf64ea582c0124da5fcfdb5a6cab',
        token='d1883cff1de9834e7c537dffb70d9dc713441e16b35e53fc8098458a44461c9b',
    )
    all_boards = client.list_boards()
    last_board = all_boards[-1]
    list = last_board.list_lists()
    board_list = []
    for entry in list:
        board_list.append((entry.id, entry.name))

    return Response(board_list)

