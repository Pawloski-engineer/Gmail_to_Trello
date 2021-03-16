from django import forms

class BoardForm(forms.ModelForm):
    class Meta:
        fields = ('flat_name', 'hosting_staircase')