from background_task import background

# @background()
# def print_sth():
#     print("hola")


from .functions import download_mails, send_mails_to_trello, change_csv_to_a_list

@background(schedule=3)
def download_some_mails(user_id):
    mails = download_mails(user_id)
    print(mails)
    trello_destinations = change_csv_to_a_list()

    for key_word_list_id_pair in trello_destinations:
        key_word = key_word_list_id_pair[0]
        list_id = key_word_list_id_pair[1]
        send_mails_to_trello(key_word, list_id, mails)


    # # TODO create new file to check iof function is called without running
    # file = open("hehe.csv", "a")
    # file.write("{key_word},{list_id}\n")
    # file.close()


