from django import forms

# class KeyWordForm(forms.Form):
#     class Meta:
#         fields = ('key_word', 'board_id', 'list_id')

class KeyWordForm(forms.Form):
    key_word = forms.CharField(max_length=100)
    board_id = forms.CharField(max_length=100)
    list_id = forms.CharField(max_length=100)


