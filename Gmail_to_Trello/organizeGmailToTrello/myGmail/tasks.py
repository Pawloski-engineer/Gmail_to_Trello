from background_task import background

# @background()
# def print_sth():
#     print("hola")


from .functions import download_mails, send_mails_to_trello

@background(schedule=3)
def download_some_mails(user_id, list_id, key_word):
    mails = download_mails(user_id)

    print(mails)

    filterdMails = mails

    print(filterdMails)

    send_mails_to_trello(key_word, list_id, filterdMails)

