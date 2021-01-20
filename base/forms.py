from django import forms
from .models import Poll

class voteForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ('question','one_choice','two_choice','three_choice')

