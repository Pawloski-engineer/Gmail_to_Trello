from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from allauth.socialaccount.models import SocialToken
from django.views.generic import ListView # only because i use CBV

# from google_auth_oauthlib.flow import
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build# from core.models import Server # whatever your custom model is you need to change accordingly
#
# # I am using a class based view. if you use DRF, or something else, you need to adapt accordingly
# class ServerList(ListView):
#     model = Server
#
#     def get_queryset(self):
#         user = self.request.user
#         result = SocialToken.objects.filter(account__user=user, account__provider="digitalocean")
#         # you can put debug points using ipdb here to check
#         return super().get_queryset()


def downloadMails(request):

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    user = request.user
    result = SocialToken.objects.filter(account__user=user, account__provider="google")[0]
    creds = Credentials. #here



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

