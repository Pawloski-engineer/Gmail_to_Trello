from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
# def main(request):

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

    # Call the Gmail API
    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])

    # Get Messages
    results = service.users().messages().list(userId='me', labelIds='INBOX').execute()
    messages = results.get('messages', [])


    # if not labels:
    #     print('No labels found.')
    # else:
    #     print('Labels:')
    #     for label in labels:
    #         print(label['name'])


    message_count = int(input("How many messages should be displayed?"))
    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        for message in messages[:message_count]:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            print(msg['snippet'])
            print('\n')
            # print("message from:")
            # print(msg['payload'])

            # print('try')
            # r = request.post('https://api.trello.com/1/cards?key=213abf64ea582c0124da5fcfdb5a6cab&token=d1883cff1de9834e7c537dffb70d9dc713441e16b35e53fc8098458a44461c9b&idList=6043a7a2e9e8ae6f9ffd133e&name=Sunday')
            # print('tried')

if __name__ == '__main__':
    # main(request='POST')
    main()
