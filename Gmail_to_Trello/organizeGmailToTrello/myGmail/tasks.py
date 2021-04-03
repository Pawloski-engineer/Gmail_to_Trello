from background_task import background

# @background()
# def print_sth():
#     print("hola")


from .functions import download_mails, send_mails_to_trello

@background(schedule=3)
def download_some_mails(user_id, list_id, key_word):
    mails = download_mails(user_id)

    print(mails)

    filterdMails = []
    for mail in mails:
        if key_word in mail:
            filterdMails.append(mail)

    print(filterdMails)
    # TODO create new file to check iof function is called without running
    file = open("hehe.csv", "a")
    file.write("{key_word},{list_id}\n")
    file.close()
    send_mails_to_trello(key_word, list_id, filterdMails)

