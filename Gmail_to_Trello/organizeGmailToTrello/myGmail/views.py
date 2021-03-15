from django.shortcuts import render

# Create your views here.

from allauth.socialaccount.models import SocialToken
# from allauth.socialaccount.providers.trello.provider import TrelloProvider #in this file there is a problrm with incorrect url
# https://github.com/pennersr/django-allauth/issues/2378

from googleapiclient.discovery import build

from google.oauth2.credentials import Credentials
from django.shortcuts import render


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
    info = {'client_id':'50255132291-r0p1je5i2il7dte7ko5u78le0r2bd82r.apps.googleusercontent.com', 'client_secret':'9Guzas1mEJK1VXDczxQY_tvT', 'refresh_token':result.token}
    creds = Credentials.from_authorized_user_info(info) #here



    service = build('gmail', 'v1', credentials=creds)

    # Get Messages
    results = service.users().messages().list(userId='me', labelIds='INBOX').execute()
    messages = results.get('messages', [])

    # message_count = request.data["message_count"] #int(input("How many messages should be displayed?"))
    message_count = 5
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
            # m = (msg['id'], msg['snippet'])
            m = (msg['snippet'])
            print(m)
            responsemessages.append(m)
            # m.save()
        # return responsemessages
        # return render(request, 'myGmail/view-mails.html', responsemessages)
        context = {
            'responsemessages': responsemessages,
        }

        return render(request, 'myGmail/view-mails.html', context)




